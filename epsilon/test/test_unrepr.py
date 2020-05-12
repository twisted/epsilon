from twisted.trial import unittest
from epsilon.unrepr import unrepr
from epsilon.compat import long

class UnreprTestCase(unittest.TestCase):

    def testSimpleUnrepr(self):
        data = {'x': [u'bob', (1+2j), []], 10: (1, {}, 'two'), (3, 4): long(5)}
        self.assertEquals(unrepr(repr(data)), data)
