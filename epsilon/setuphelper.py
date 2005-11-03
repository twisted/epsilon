
# For great justice, take off every zig.
import sys, os, pprint

from distutils.core import setup

def regeneratePluginCache(dist):
    if 'install' in dist.commands:
        sys.path.insert(0, dist.command_obj['install'].install_lib)
        print 'Regenerating cache with path: ',
        pprint.pprint(sys.path)
        from twisted import plugin
        from axiom import plugins
        # Not just *some* zigs, mind you - *every* zig:
        print 'Full plugin list: ',
        pprint.pprint(list(plugin.getPlugins(plugin.IPlugin, plugins)))

def autosetup(**kw):
    packages = []
    datafiles = {}

    for (dirpath, dirnames, filenames) in os.walk(os.curdir):
        dirnames[:] = [p for p in dirnames if not p.startswith('.')]
        if '__init__.py' in filenames:
            # The current directory is a Python package
            packages.append(dirpath[2:].replace('/', '.'))
    for package in packages:
        if '.' in package:
            continue
        D = datafiles[package] = []
        print os.listdir(package)
        for (dirpath, dirnames, filenames) in os.walk(package):
            dirnames[:] = [p for p in dirnames if not p.startswith('.')]
            for filename in filenames:
                if filename == 'dropin.cache':
                    continue
                if (os.path.splitext(filename)[1] not in ('.py', '.pyc', '.pyo')
                    or '__init__.py' not in filenames):
                    D.append(os.path.join(dirpath[len(package)+1:], filename))
    autoresult = {
        'packages': packages,
        'package_data': datafiles,
        }
    print 'Automatically determined setup() args:'
    pprint.pprint(autoresult, indent=4)
    assert 'packages' not in kw
    assert 'package_data' not in kw
    kw.update(autoresult)
    distobj = setup(**kw)
    regeneratePluginCache(distobj)
    return distobj
