from six.moves import builtins


def _cmp(x, y):
    return (x > y) - (x < y)


cmp = getattr(builtins, 'cmp', _cmp)
long = getattr(builtins, 'long', int)
