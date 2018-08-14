
class OnlyMeta(type):
    def __new__(cls, name, bases, classdict):
        # Disallow bases that have __new__ or __init__ defined
        for b in bases:
            if not isinstance(b, cls):
                if b.__init__ is not object.__init__:
                    raise TypeError("Class Only classes cannot define __init__", b)
                if b.__new__ is not object.__new__:
                    raise TypeError("Class Only classes cannot define __new__", b)
        return super().__new__(cls, name, bases, classdict)

    def __setattr__(cls, name, arg):
        if not getattr(cls, "_initializing_", False):
            raise TypeError("Class Only classes are immutable")
        return super().__setattr__(name, arg)


class MetaNamespace(core.OnlyMeta):
    def __new__(cls, name, bases, classdict):
        # disallow reserved names
        for b in bases:
            if not isinstance(b, cls):
                bad_names = vars(b).keys() & constants.RESERVED_NAMES
                if bad_names:
                    raise ValueError(
                        "Cannot create namespace class with reserved names",
                        sorted(bad_names),
                    )
        return super().__new__(cls, name, bases, classdict)

    def __iter__(cls):
        # Walk up the mro, looking for namespace classes. Keep track of attrs we've already seen
        # and don't re-yield their values
        seen_attrs = set()
        for c in cls.__mro__:
            if issubclass(type(c), type(cls)):
                # c is the class created by the namespace decorator, so look one level up to find
                # the decorated class. This will mean that classes that inherit from namespaces
                # aren't iterable unless they're @namespace decorated
                for k, v in vars(c.__mro__[1]).items():
                    if not _is_internal(k) and k not in seen_attrs:
                        seen_attrs.add(k)
                        yield v
