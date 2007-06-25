
"""
failUnlessWarns assertion from twisted.trial in the pending 2.6 release.

This is from r20538; it should be updated as bugfixes are made.
"""

import warnings
from pprint import pformat

def failUnlessWarns(self, category, message, filename, f,
                   *args, **kwargs):
    """
    Fail if the given function doesn't generate the specified warning when
    called. It calls the function, checks the warning, and forwards the
    result of the function if everything is fine.

    @param category: the category of the warning to check.
    @param message: the output message of the warning to check.
    @param filename: the filename where the warning should come from.
    @param f: the function which is supposed to generate the warning.
    @type f: any callable.
    @param args: the arguments to C{f}.
    @param kwargs: the keywords arguments to C{f}.

    @return: the result of the original function C{f}.
    """
    warningsShown = []
    def showwarning(*args):
        warningsShown.append(args)

    origshow = warnings.showwarning
    globs = f.func_globals
    origregistry = globs.get('__warningregistry__', {})
    try:
        warnings.showwarning = showwarning
        globs['__warningregistry__'] = {}
        result = f(*args, **kwargs)
    finally:
        warnings.showwarning = origshow
        globs['__warningregistry__'] = origregistry

    self.assertEqual(len(warningsShown), 1, pformat(warningsShown))
    gotMessage, gotCategory, gotFilename, lineno = warningsShown[0]
    self.assertEqual(gotMessage.args, message)
    self.assertIdentical(gotCategory, category)

    # Use starts with because of .pyc/.pyo issues.
    self.failUnless(
        filename.startswith(gotFilename),
        'Warning in %r, expected %r' % (gotFilename, filename))

    # It would be nice to be able to check the line number as well, but
    # different configurations actually end up reporting different line
    # numbers (generally the variation is only 1 line, but that's enough
    # to fail the test erroneously...).
    # self.assertEqual(lineno, xxx)

    return result

def install():
    from twisted.trial.unittest import TestCase
    TestCase.failUnlessWarns = TestCase.assertWarns = failUnlessWarns
