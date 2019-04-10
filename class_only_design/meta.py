from class_only_design import constants
from class_only_design import util

# This is inserted into decorated classes. Note, __new__ is implicitly converted to a staticmethod
# during class creation. I'm doing so explicitly here so I have a reference I can check later. This
# seems to prevent the implicit transformation, but I'm not sure if that's an implementation
# detail.
@staticmethod
def __new__(*args, **kwargs):
    raise TypeError("Class Only classes cannot be instantiated")


class OnlyMeta(type):
    def __new__(cls, name, bases, classdict):

        if "__init__" in classdict:
            raise TypeError("Class Only classes cannot define __init__")
        if classdict.get("__new__") not in (__new__, None):
            raise TypeError("Class Only classes cannot define __new__")

        # Disallow bases that have __new__ or __init__ defined
        for b in bases:
            if not isinstance(b, cls):
                if b.__init__ is not object.__init__:
                    raise TypeError("Class Only classes cannot define __init__", b)
                if b.__new__ is not object.__new__:
                    raise TypeError("Class Only classes cannot define __new__", b)

        # Insert our own __new__
        classdict["__new__"] = __new__
        return super().__new__(cls, name, bases, classdict)

    def __setattr__(cls, name, arg):
        if not getattr(cls, "_initializing_", False):
            raise TypeError("Class Only classes are immutable")
        return super().__setattr__(name, arg)


class MetaNamespace(OnlyMeta):
    def __new__(cls, name, bases, classdict):
        # disallow reserved names
        bad_names = classdict.keys() & constants.RESERVED_NAMES

        for b in bases:
            if not isinstance(b, cls):
                bad_names |= vars(b).keys() & constants.RESERVED_NAMES
        if bad_names:
            raise ValueError(
                "Cannot create namespace class with reserved names", sorted(bad_names)
            )
        classdict['_initializing_'] = True
        created_class = super().__new__(cls, name, bases, classdict)
        created_class.nameof = util.KeyGetter(created_class)
        del created_class._initializing_
        return created_class

    def __iter__(cls):
        # Walk up the mro, looking for namespace classes. Keep track of attrs we've already seen
        # and don't re-yield their values
        seen_attrs = set()
        for c in cls.__mro__:
            if isinstance(c, MetaNamespace):
                for k, v in vars(c).items():
                    if not util._is_internal(k) and k not in seen_attrs:
                        seen_attrs.add(k)
                        yield v

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return util.NamespaceLoader()
