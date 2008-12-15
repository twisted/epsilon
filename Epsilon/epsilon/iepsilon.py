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

        @param pads: Mapping between all valid C{str} one-time pads and their
            C{str} avatar IDs.
        @type pads: C{dict}

        @return: This pad's value in C{pads}, or C{None} if the pad is not
            valid.
        @rtype: C{str} or C{NoneType}
        """
