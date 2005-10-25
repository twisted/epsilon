
from twisted.trial import unittest

from epsilon.modal import mode, ModalType

class ModalTestClass(object):
    __metaclass__ = ModalType

    modeAttribute = 'mode'
    initialMode = 'alpha'

    class alpha(mode):
        def one(self):
            return 'alpha-one'
        def two(self):
            return 'alpha-two'

    class beta(mode):
        def two(self):
            return 'beta-two'
        def three(self):
            return 'beta-three'

    def four(self):
        return 'unmode-four'

    class gamma(mode):
        def change(self):
            self.mode = 'delta'
            return self.change()

    class delta(mode):
        def change(self):
            return 'delta-change'

class ModalityTestCase(unittest.TestCase):
    def testModalMethods(self):
        x = ModalTestClass()
        self.assertEquals(x.one(), 'alpha-one')
        self.assertEquals(x.two(), 'alpha-two')
        self.assertRaises(AttributeError, getattr, x, 'three')
        self.assertEquals(x.four(), 'unmode-four')

        x.mode = 'beta'
        self.assertRaises(AttributeError, getattr, x, 'one')
        self.assertEquals(x.two(), 'beta-two')
        self.assertEquals(x.three(), 'beta-three')
        self.assertEquals(x.four(), 'unmode-four')

    def testInternalModeChange(self):
        x = ModalTestClass()
        x.mode = 'gamma'
        self.assertEquals(x.change(), 'delta-change')
