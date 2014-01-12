"""
Tests for turning simple version strings into twisted.python.versions.Version
objects.

"""
from epsilon import asTwistedVersion
from twisted.trial.unittest import SynchronousTestCase


class AsTwistedVersionTests(SynchronousTestCase):
    def test_simple(self):
        """
        A simple version string can be turned into a Version object.
        """
        version = asTwistedVersion("package", "1.2.3")
        self.assertEqual(version.package, "package")
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.micro, 3)
