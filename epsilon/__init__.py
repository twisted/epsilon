# -*- test-case-name: epsilon.test -*-
from epsilon._version import __version__

def asTwistedVersion(packageName, versionString):
    from twisted.python import versions
    import re
    return versions.Version(
        packageName,
        *map(int, re.match(r"[0-9.]*", versionString).group().split(".")[:3]))

version = asTwistedVersion("epsilon", __version__)
__all__ = ['__version__', 'version']
