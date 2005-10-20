import new
class ModalMethod(object):
    """A descriptor wrapping multiple implementations of a particular method.

    When called on an instance, the implementation used will be
    selected based on an attribute of the instance.  There are no
    unbound ModalMethods at this point.

    @ivar name: The name of this method.
    @ivar methods: A mapping of modes to callable objects.

    @ivar modeAttribute: The name of the attribute on instances which
    is bound to the instance's current mode.
    """

    def __init__(self, name, methods, modeAttribute):
        self.name = name
        self.methods = methods
        self.modeAttribute = modeAttribute

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError(self.name)
        try:
            mode = getattr(instance, self.modeAttribute)
        except AttributeError:
            raise AttributeError(
                "Mode attribute %r missing from %r, "
                "cannot get %r" % (self.modeAttribute, instance, self.name))

        try:
            func = self.methods[mode]
        except KeyError:
            raise AttributeError(
                "Method %r missing from mode %r on %r" % (self.name, mode, instance))

        return new.instancemethod(func, instance, owner)

class mode(object):
    """
    Base class for mode definitions.  Subclass this in classes of type
    ModalType and provide the implementations of various methods for
    that particular mode as methods of the mode subclass.  The
    subclass should have the same name as the mode it is defining.
    """

class ModalType(type):
    """Metaclass for defining modal classes.

    @type modeAttribute: C{str}
    @ivar modeAttribute: The attribute to which the current mode is
    bound.  Classes should not define the attribute this names; it
    will be bound automatically to the value of initialMode.

    @type initialMode: C{str} (for now)
    @ivar initialMode: The mode in which instances will start.
    """
    def __new__(cls, name, bases, attrs):
        try:
            # XXX This is wrong: it does not respect inherited
            # mode attribute settings.  Fix it when someone wants
            # inherited mode attributes to work.
            modeAttribute = attrs.pop('modeAttribute')
        except KeyError:
            raise TypeError("%r does not define required modeAttribute." % (name,))

        try:
            initialMode = attrs['initialMode']
        except KeyError:
            raise TypeError("%r does not defing require initialMode." % (name,))

        # Dict mapping names of methods to another dict.  The inner
        # dict maps names of modes to implementations of that method
        # for that mode.
        implementations = {}

        keepAttrs = {'mode': initialMode}
        for (k, v) in attrs.iteritems():
            if isinstance(v, type) and issubclass(v, mode):
                for (methName, methDef) in v.__dict__.iteritems():
                    implementations.setdefault(methName, {})[k] = methDef
            else:
                keepAttrs[k] = v

        for (methName, methDefs) in implementations.iteritems():
            keepAttrs[methName] = ModalMethod(methName, methDefs, modeAttribute)

        return super(ModalType, cls).__new__(cls, name, bases, keepAttrs)
