
from twisted.trial import unittest
from epsilon.structlike import record


class StructLike(unittest.TestCase):
    def _testme(self, TestStruct):
        x = TestStruct()
        self.assertEquals(x.x, 1)
        self.assertEquals(x.y, 2)
        self.assertEquals(x.z, 3)

        y = TestStruct('3', '2', '1')
        self.assertEquals(y.x, '3')
        self.assertEquals(y.y, '2')
        self.assertEquals(y.z, '1')

        z = TestStruct(z='z', x='x', y='y')
        self.assertEquals(z.x, 'x')
        self.assertEquals(z.y, 'y')
        self.assertEquals(z.z, 'z')

        a = TestStruct('abc')
        self.assertEquals(a.x, 'abc')
        self.assertEquals(a.y, 2)
        self.assertEquals(a.z, 3)

        b = TestStruct(y='123')
        self.assertEquals(b.x, 1)
        self.assertEquals(b.y, '123')
        self.assertEquals(b.z, 3)

    def testWithPositional(self):
        self._testme(record('x y z', x=1, y=2, z=3))

    def testWithPositionalSubclass(self):
        class RecordSubclass(record('x y z', x=1, y=2, z=3)):
            pass
        self._testme(RecordSubclass)

    def testWithoutPositional(self):
        self._testme(record(x=1, y=2, z=3))

    def testWithoutPositionalSubclass(self):
        class RecordSubclass(record(x=1, y=2, z=3)):
            pass
        self._testme(RecordSubclass)

    def testBreakRecord(self):
        self.assertRaises(TypeError, record)
        self.assertRaises(TypeError, record, 'a b c', a=1, c=2)
        self.assertRaises(TypeError, record, 'a b', c=2)
        self.assertRaises(TypeError, record, 'a b', a=1)

    def testUndeclared(self):
        R = record('a')
        r = R(1)
        r.foo = 2
        self.assertEquals(r.foo, 2)

    def testCreateWithNoValuesAndNoDefaults(self):
        R = record('x')
        self.assertRaises(TypeError, R)
