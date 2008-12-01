# Copyright (c) 2008 Divmod.  See LICENSE for details.

"""
Epsilon interfaces.
"""
from zope.interface import Attribute

from twisted.cred.credentials import ICredentials


class IOneTimePad(ICredentials):
    """
    A type of opaque credential for authenticating users, which can be used
    only a single time.
    """
    def checkPad(pads):
        """
        Validate this pad against all known one-time pads.  If there is a
        match, login will be successful and this pad will be invalidated
        (further attempts to use it will fail).

        @param pads: Container of all valid C{str} one-time pads.
        @type pads: C{dict}

        @rtype: C{bool}
        """
