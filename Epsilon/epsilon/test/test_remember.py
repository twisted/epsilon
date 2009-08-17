
from twisted.trial.unittest import TestCase

from epsilon.remember import remembered
from epsilon.structlike import record

class Rememberee(record("rememberer whichValue")):
    """
    A sample value that holds on to its L{Rememberer}.
    """


class Rememberer(object):
    """
    Sample application code which uses epsilon.remember.

    @ivar invocations: The number of times that it is invoked.
    """

    invocations = 0
    otherInvocations = 0

    @remembered
    def value1(self):
        """
        I remember a value.
        """
        self.invocations += 1
        return Rememberee(self, 1)


    @remembered
    def value2(self):
        """
        A separate value.
        """
        self.otherInvocations += 1
        return Rememberee(self, 2)


class RememberedTests(TestCase):
    """
    The "remembered" decorator allows you to lazily create an attribute and
    remember it.
    """

    def setUp(self):
        """
        Create a L{Rememberer} for use with the tests.
        """
        self.rememberer = Rememberer()


    def test_selfArgument(self):
        """
        The "self" argument to the decorated creation function will be the
        instance the property is accessed upon.
        """
        value = self.rememberer.value1
        self.assertIdentical(value.rememberer, self.rememberer)


    def test_onlyOneInvocation(self):
        """
        The callable wrapped by C{@remembered} will only be invoked once,
        regardless of how many times the attribute is accessed.
        """
        self.assertEquals(self.rememberer.invocations, 0)
        firstTime = self.rememberer.value1
        self.assertEquals(self.rememberer.invocations, 1)
        secondTime = self.rememberer.value1
        self.assertEquals(self.rememberer.invocations, 1)
        self.assertIdentical(firstTime, secondTime)


    def test_twoValues(self):
        """
        If the L{@remembered} decorator is used more than once, each one will
        be an attribute with its own identity.
        """
        self.assertEquals(self.rememberer.invocations, 0)
        self.assertEquals(self.rememberer.otherInvocations, 0)
        firstValue1 = self.rememberer.value1
        self.assertEquals(self.rememberer.invocations, 1)
        self.assertEquals(self.rememberer.otherInvocations, 0)
        firstValue2 = self.rememberer.value2
        self.assertEquals(self.rememberer.otherInvocations, 1)
        self.assertNotIdentical(firstValue1, firstValue2)
        secondValue2 = self.rememberer.value2
        self.assertIdentical(firstValue2, secondValue2)
