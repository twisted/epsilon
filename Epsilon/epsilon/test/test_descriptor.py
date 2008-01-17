"""
Tests for L{epsilon.descriptor}.
"""
from twisted.trial import unittest

from epsilon import descriptor

class Test1(object):
    class a(descriptor.attribute):
        def get(self):
            return 1
        def set(self, value):
            pass
        def delete(self):
            pass


class Test2(object):
    class a(descriptor.attribute):
        "stuff"
        def get(self):
            return 10


class DescriptorTest(unittest.TestCase):
    def testCase1(self):
        t = Test1()
        self.assertEquals(t.a, 1)
        t.a = 2
        self.assertEquals(t.a, 1)
        del t.a
        self.assertEquals(t.a, 1)


    def testCase2(self):
        t = Test2()
        self.assertEquals(Test2.a.__doc__, 'stuff')
        self.assertEquals(t.a, 10)
        def _(): t.a = 1
        self.assertRaises(AttributeError, _)
        def _(): del t.a
        self.assertRaises(AttributeError, _)



class AbstractFoo:
    """
    Toy class used by L{RequiredAttributeTestCase}.
    """
    foo = descriptor.requiredAttribute('foo')



class ManifestFoo(AbstractFoo):
    """
    Toy class used by L{RequiredAttributeTestCase}.
    """
    foo = 'bar'



class RequiredAttributeTestCase(unittest.TestCase):
    """
    Tests for L{descriptor.requiredAttribute}.
    """
    def test_defaultAccess(self):
        """
        Accessing a L{descriptor.requiredAttribute} should throw a
        C{AttributeError} if its value has not been overridden.
        """
        abstractFoo = AbstractFoo()
        exception = self.assertRaises(AttributeError, lambda: abstractFoo.foo)
        self.assertEqual(len(exception.args), 1)
        self.assertEqual(
            exception.args[0],
            ("Required attribute 'foo' has not been changed"
                " from its default value on %r" % (abstractFoo,)))


    def test_derivedAccess(self):
        """
        If a derived class sets a new value for a
        L{descriptor.requiredAttribute}, things should work fine.
        """
        manifestFoo = ManifestFoo()
        self.assertEqual(manifestFoo.foo, 'bar')
