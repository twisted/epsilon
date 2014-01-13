# -*- test-case-name: epsilon.test -*-
from epsilon._version import __version__
from twisted.python import versions

def asTwistedVersion(packageName, versionString):
    return versions.Version(packageName, *map(int, versionString.split(".")))

version = asTwistedVersion("epsilon", __version__)
