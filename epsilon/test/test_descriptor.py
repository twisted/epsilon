
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
