import functools

from class_only_design import core
from class_only_design import constants


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return (
        name[:2] == name[-2:] == "__"
        and name[2:3] != "_"
        and name[-3:-2] != "_"
        and len(name) > 4
    )


def _is_sunder(name):
    """Returns True if a _sunder_ name, False otherwise."""
    return (
        name[0] == name[-1] == "_"
        and name[1:2] != "_"
        and name[-2:-1] != "_"
        and len(name) > 2
    )


def _is_reserved(name):
    return name in constants.RESERVED_NAMES


def _is_internal(name):
    """Return true if the given name is internal to the class_only_design library. Currently we
    check for __dunder__ and _sunder_ names
    """
    return _is_dunder(name) or _is_sunder(name) or _is_reserved(name)


class KeyGetter:
    def __init__(self, cls):
        """
        KeyGetter takes a class, and provides a __getattr__ that returns keys instead of values
        """
        self._cls_ = cls

    def __getattr__(self, attr):
        # Call getattr, so that an exception is raised as normal if the attr doesn't exist
        getattr(self._cls_, attr)
        return attr


class MetaNamespace(core.OnlyMeta):
    def __new__(cls, name, bases, classdict):
        # disallow reserved names
        for b in bases:
            if not isinstance(b, cls):
                bad_names = vars(b).keys() & constants.RESERVED_NAMES
                if bad_names:
                    raise ValueError(
                        "Cannot create namespace class with reserved names", bad_names
                    )
        return super().__new__(cls, name, bases, classdict)

    def __iter__(cls):
        for c in cls.__mro__:
            if issubclass(type(c), type(cls)):
                # c is the class created by the namespace decorator, so look one level up to find
                # the decorated class. This will mean that classes that inherit from namespaces
                # aren't iterable unless they're @namespace decorated
                for k, v in vars(c.__mro__[1]).items():
                    if not _is_internal(k):
                        yield v


def namespace(cls):
    """
    Class only is a class decorator that disallows instantiation or state change on a class object.
    """
    # set updated to an empty iterable. By default wraps attempts to update __dict__, which isn't
    # valid on a class
    @functools.wraps(cls, updated=())
    class NS(cls, metaclass=MetaNamespace):
        _initializing_ = True

        def __new__(*args, **kwargs):
            raise TypeError("Class Only classes cannot be instantiated")

        nameof = KeyGetter(cls)

    del NS._initializing_
    return NS
