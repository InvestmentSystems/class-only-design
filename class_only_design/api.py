import functools

from class_only_design.meta import OnlyMeta
from class_only_design.meta import MetaNamespace


def class_only(cls):
    """
    Class only is a class decorator that disallows instantiation or state change on a class object.
    """
    # set updated to an empty iterable. By default wraps attempts to update __dict__, which isn't
    # valid on a class
    @functools.wraps(cls, updated=())
    class Only(cls, metaclass=OnlyMeta):
        _initializing_ = True

        def __new__(*args, **kwargs):
            raise TypeError("Class Only classes cannot be instantiated")

    del Only._initializing_
    return Only


class constant:
    """
    A method decorator similar to @property but for use on class only classes. The decorated method
    is only called once. Subsequent calls simply return the stored value. This is usefull for
    declaring a class level constant that is not actually created until it's used.
    """

    def __init__(self, method):
        self.method = method
        self._value = None

    def __get__(self, instance, cls):
        if not self._value:
            self._value = self.method(cls)
        return self._value


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
