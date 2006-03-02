
class NoSuchHotfix(Exception):
    """
    Man you must be pretty stupid.
    """

_alreadyInstalled = set()
def require(packageName, fixName):
    if (packageName, fixName) in _alreadyInstalled:
        return

    if (packageName, fixName) == ('twisted', 'filepath_copyTo'):
        from twisted.python import filepath
        if filepath.FilePath('a') != filepath.FilePath('a'):
            from epsilon.hotfixes import filepath_copyTo
            filepath_copyTo.install()
    elif (packageName, fixName) == ('twisted', 'stdio_getPeer'):
        from twisted.internet import stdio
        if 'getPeer' not in vars(stdio.StandardIO):
            from epsilon.hotfixes import stdio_getPeer
            print 'Installing getpeer fix'
            stdio_getPeer.install()
    else:
        raise NoSuchHotfix(packageName, fixName)

    _alreadyInstalled.add((packageName, fixName))
