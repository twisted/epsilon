
import inspect

class NoSuchHotfix(Exception):
    """
    Man you must be pretty stupid.
    """

_alreadyInstalled = set()
def require(packageName, fixName):
    if (packageName, fixName) in _alreadyInstalled:
        return

    if (packageName, fixName) == ('twisted', 'filepath_copyTo'):
        from twisted.python import filepath
        if filepath.FilePath('a') != filepath.FilePath('a'):
            from epsilon.hotfixes import filepath_copyTo
            filepath_copyTo.install()
    elif (packageName, fixName) == ('twisted', 'timeoutmixin_calllater'):
        from twisted.protocols import policies
        if not hasattr(policies.TimeoutMixin, 'callLater'):
            from epsilon.hotfixes import timeoutmixin_calllater
            timeoutmixin_calllater.install()
    elif (packageName, fixName) == ('twisted', 'delayedcall_seconds'):
        from twisted.internet import base
        args = inspect.getargs(base.DelayedCall.__init__.func_code)[0]
        if 'seconds' not in args:
            from epsilon.hotfixes import delayedcall_seconds
            delayedcall_seconds.install()
    elif (packageName, fixName) == ('twisted', 'deferredgenerator_tfailure'):
        from twisted.internet import defer
        result = []
        def test():
            d = defer.waitForDeferred(defer.succeed(1))
            yield d
            result.append(d.getResult())
        defer.deferredGenerator(test)()
        if result == [1]:
            from epsilon.hotfixes import deferredgenerator_tfailure
            deferredgenerator_tfailure.install()
        else:
            assert result == [None]
    elif (packageName, fixName) == ("twisted", "proto_helpers_stringtransport"):
        from twisted.test.proto_helpers import StringTransport
        st = StringTransport()
        try:
            st.write(u'foo')
        except TypeError, e:
            pass
        else:
            from epsilon.hotfixes import proto_helpers_stringtransport
            proto_helpers_stringtransport.install()
        
    else:
        raise NoSuchHotfix(packageName, fixName)

    _alreadyInstalled.add((packageName, fixName))
