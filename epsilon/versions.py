# -*- test-case-name: epsilon.test.test_versions -*-

class IncomparableVersions(TypeError):
    """
    Two versions could not be compared.
    """

class Version(object):
    def __init__(self, package, major, minor, micro):
        self.package = package
        self.major = major
        self.minor = minor
        self.micro = micro

    def __repr__(self):
        return '%s(%r, %d, %d, %d)' % (
            self.__class__.__name__,
            self.major,
            self.minor,
            self.micro)

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.package != other.package:
            raise IncomparableVersions()
        return cmp((self.major,
                    self.minor,
                    self.micro),
                   (other.major,
                    other.minor,
                    other.micro))
