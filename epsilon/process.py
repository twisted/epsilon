import os, sys, imp, sets
from epsilon.modal import ModalType, mode
from vertex import juice
from twisted.python import procutils, log
from twisted.internet import reactor, protocol, defer

def spawnProcess(processProtocol, executable, args=(), env={},
                 path=None, uid=None, gid=None, usePTY=0,
                 packages=()):
    """Launch a process with a particular Python environment.

    All arguments as to reactor.spawnProcess(), except for the
    addition of an optional packages iterable.  This should be
    of strings naming packages the subprocess is to be able to
    import.
    """

    env = env.copy()

    pythonpath = []
    for pkg in packages:
        p = os.path.split(imp.find_module(pkg)[1])[0]
        if p.startswith(os.path.join(sys.prefix, 'lib')):
            continue
        pythonpath.append(p)
    pythonpath = list(sets.Set(pythonpath))
    pythonpath.extend(env.get('PYTHONPATH', '').split(os.pathsep))
    env['PYTHONPATH'] = os.pathsep.join(pythonpath)

    return reactor.spawnProcess(processProtocol, executable, args,
                                env, path, uid, gid, usePTY)

def spawnPythonProcess(processProtocol, args=(), env={},
                       path=None, uid=None, gid=None, usePTY=0,
                       packages=()):
    """Launch a Python process

    All arguments as to spawnProcess(), except the executable
    argument is omitted.
    """
    return spawnProcess(processProtocol, sys.executable,
                        args, env, path, uid, gid, usePTY,
                        packages)


class ProcessUnavailable(Exception):
    """Indicates the process is not available to perform tasks.

    This is a transient error.  Calling code should handle it by
    arranging to do the work they planned on doing at a later time.
    """


class Shutdown(juice.Command):
    """
    Abandon, belay, cancel, cease, close, conclude, cut it out, desist,
    determine, discontinue, drop it, end, finish, finish up, give over, go
    amiss, go astray, go wrong, halt, have done with, hold, knock it off, lay
    off, leave off, miscarry, perorate, quit, refrain, relinquish, renounce,
    resolve, scrap, scratch, scrub, stay, stop, terminate, wind up.
    """
    commandName = "Shutdown"
    responseType = juice.QuitBox


def _childProcTerminated(self, err):
    self.mode = 'stopped'
    err = ProcessUnavailable(err)
    for d in self.waitingForProcess:
        d.errback(err)
    del self.waitingForProcess

class ProcessController(object):
    """Stateful class which tracks a Juice connection to a child process.

    Communication occurs over stdin and stdout of the child process.  The
    process is launched and restarted as necessary.  Failures due to the child
    process terminating, either unilaterally of by request, are represented as
    a transient exception class,

    Mode is one of
      'stopped'       (no process running or starting)
      'starting'      (process begun but not ready for requests)
      'ready'         (process ready for requests)
      'stopping'      (process being torn down)
      'waiting_ready' (process beginning but will be shut down
                          as soon as it starts up)

    Transitions are as follows

       getProcess:
           stopped -> starting:
               launch process
               create/save in waitingForStartup/return Deferred
           starting -> starting:
               create/save/return Deferred
           ready -> ready:
                return saved process
           stopping:
                return failing Deferred indicating transient failure
           waiting_ready:
                return failing Deferred indicating transient failure

       stopProcess:
           stopped -> stopped:
               return succeeding Deferred
           starting -> waiting_ready:
               create Deferred, add transient failure errback handler, return
           ready -> stopping:
               call shutdown on process
               return Deferred which fires when shutdown is done

       childProcessCreated:
           starting -> ready:
               callback saved Deferreds
               clear saved Deferreds
           waiting_ready:
               errback saved Deferred indicating transient failure
               return _shutdownIndexerProcess()

       childProcessTerminated:
           starting -> stopped:
               errback saved Deferreds indicating transient failure
           waiting_ready -> stopped:
               errback saved Deferreds indicating transient failure
           ready -> stopped:
               drop reference to process object
           stopping -> stopped:
               Callback saved shutdown deferred

    @ivar process: A reference to the process object.  Set in every non-stopped
    mode.

    @ivar broker: A reference to the perspective broker.  Set in the ready
    mode.

    @ivar root: A reference to the root of the remote object graph.  Set in the
    ready mode.

    @ivar connector: A reference to the process protocol.  Set in every
    non-stopped mode.

    @ivar onProcessStartup: None or a callable which will be invoked with the
    root object whenever a Juice connection is first established to a newly
    spawned child process.
    """

    __metaclass__ = ModalType

    initialMode = 'stopped'
    modeAttribute = 'mode'

    # A reference to the Twisted process object which corresponds to
    # the child process we have spawned.  Set to a non-None value in
    # every state except stopped.
    process = None

    # A reference to the process protocol object via which we
    # communicate with the process's stdin and stdout.  Set to a
    # non-None value in every state except stopped.
    connector = None

    def __init__(self, name, juice, tacPath, onProcessStartup=None):
        # Primarily, keep the indexer in memory, which will in turn
        # keep a reference to us, which basically results in the whole
        # setup remaining in memory for the duration of the process
        # lifecycle.
        self.name = name
        self.onProcessStartup = onProcessStartup
        self.juice = juice
        self.tacPath = tacPath

    def _startProcess(self):
        executable = sys.executable
        env = os.environ
        env['PYTHONPATH'] = os.pathsep.join(sys.path)

        twistdBinaries = procutils.which("twistd2.4") + procutils.which("twistd")
        if not twistdBinaries:
            return defer.fail(RuntimeError("Couldn't find twistd to start subprocess"))
        twistd = twistdBinaries[0]

        setsid = procutils.which("setsid")

        self.connector = JuiceConnector(self.juice, self)

        args = (
            sys.executable,
            twistd,
            '--logfile=%s.%d.log' % (self.name, os.getpid()),
            '--pidfile=%s.%d.pid' % (self.name, os.getpid()),
            '-noy',
            self.tacPath)

        if setsid:
            args = ('setsid',) + args
            executable = setsid[0]

        self.process = spawnProcess(
            self.connector, executable, args, env=env)

    class stopped(mode):
        def getProcess(self):
            self.mode = 'starting'
            self.waitingForProcess = []

            self._startProcess()

            # Mode has changed, this will call some other
            # implementation of getProcess.
            return self.getProcess()

        def stopProcess(self):
            return defer.succeed(None)

    class starting(mode):
        def getProcess(self):
            d = defer.Deferred()
            self.waitingForProcess.append(d)
            return d

        def stopProcess(self):
            def eb(err):
                err.trap(ProcessUnavailable)

            d = defer.Deferred().addErrback(eb)
            self.waitingForProcess.append(d)

            self.mode = 'waiting_ready'
            return d

        def childProcessCreated(self):
            self.mode = 'ready'

            if self.onProcessStartup is not None:
                self.onProcessStartup(self.juice)

            for d in self.waitingForProcess:
                d.callback(self.juice)
            del self.waitingForProcess

        childProcessTerminated = _childProcTerminated


    class ready(mode):
        def getProcess(self):
            return defer.succeed(self.juice)

        def stopProcess(self):
            self.mode = 'stopping'
            self.onShutdown = defer.Deferred()
            Shutdown().do(self.juice)
            return self.onShutdown

        def childProcessTerminated(self, reason):
            self.mode = 'stopped'
            self.process = self.connector = None


    class stopping(mode):
        def getProcess(self):
            return defer.fail(ProcessUnavailable("Shutting down"))

        def stopProcess(self):
            return self.onShutdown

        def childProcessTerminated(self, reason):
            self.mode = 'stopped'
            self.process = self.connector = None
            self.onShutdown.callback(None)


    class waiting_ready(mode):
        def getProcess(self):
            return defer.fail(ProcessUnavailable("Shutting down"))

        def childProcessCreated(self):
            # This will put us into the stopped state - no big deal,
            # we are going into the ready state as soon as it returns.
            _childProcTerminated(self, RuntimeError("Shutting down"))

            # Dip into the ready mode for ever so brief an instant so
            # that we can shut ourselves down.
            self.mode = 'ready'
            return self.stopProcess()

        childProcessTerminated = _childProcTerminated


class JuiceConnector(protocol.ProcessProtocol):

    def __init__(self, proto, controller):
        self.juice = proto
        self.controller = controller

    def connectionMade(self):
        log.msg("Subprocess started.")
        self.juice.makeConnection(self)
        self.controller.childProcessCreated()

    # Transport
    disconnecting = False

    def write(self, data):
        self.transport.write(data)

    def writeSequence(self, data):
        self.transport.writeSequence(data)

    def loseConnection(self):
        self.transport.loseConnection()

    def getPeer(self):
        return ('omfg what are you talking about',)

    def getHost(self):
        return ('seriously it is a process this makes no sense',)

    def inConnectionLost(self):
        log.msg("Standard in closed")
        protocol.ProcessProtocol.inConnectionLost(self)

    def outConnectionLost(self):
        log.msg("Standard out closed")
        protocol.ProcessProtocol.outConnectionLost(self)

    def errConnectionLost(self):
        log.msg("Standard err closed")
        protocol.ProcessProtocol.errConnectionLost(self)

    def outReceived(self, data):
        self.juice.dataReceived(data)

    def errReceived(self, data):
        log.msg("Received stderr from subprocess: " + repr(data))

    def processEnded(self, status):
        log.msg("Process ended")
        self.juice.connectionLost(status)
        self.controller.childProcessTerminated(status)


class JuiceChild(juice.Juice):
    """
    Protocol class which runs in the child process

    This just defines one behavior on top of a regular juice protocol: the
    shutdown command, which drops the connection and stops the reactor.
    """
    shutdown = False

    def connectionLost(self, reason):
        juice.Juice.connectionLost(self, reason)
        if self.shutdown:
            reactor.stop()

    def command_SHUTDOWN(self):
        log.msg("Shutdown message received, goodbye.")
        self.shutdown = True
        return {}
    command_SHUTDOWN.command = Shutdown
