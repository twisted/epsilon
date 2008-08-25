# Copyright (c) 2008 Divmod.  See LICENSE for details.

"""
An AMP client which connects to and authenticates with an AMP server, then
issues a command.
"""

from twisted.internet.protocol import ClientCreator
from twisted.internet import reactor
from twisted.cred.credentials import UsernamePassword
from twisted.protocols.amp import AMP

from epsilon.ampauth import login

from auth_server import Add


def add(proto):
    return proto.callRemote(Add, left=17, right=33)


def display(result):
    print result


def error(err):
    print err.getErrorMessage()


def finish(ignored):
    reactor.stop()


def main():
    cc = ClientCreator(reactor, AMP)
    d = cc.connectTCP('localhost', 7805)
    d.addCallback(login, UsernamePassword("testuser", "examplepass"))
    d.addCallback(add)
    d.addCallback(display)
    d.addErrback(error)
    d.addCallback(finish)
    reactor.run()


if __name__ == '__main__':
    main()
