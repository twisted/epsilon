
# For great justice, take off every zig.
import sys, os, pprint

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
