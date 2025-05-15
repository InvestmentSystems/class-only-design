import functools

from class_only_design.meta import OnlyMeta
from class_only_design.meta import MetaNamespace
from class_only_design import util


class ClassOnly(metaclass=OnlyMeta):
    """
    ClassOnly classes disallow instantiation or state change.
    """


class Namespace(metaclass=MetaNamespace):
    """
    Namespace classes are intended for storing symbolic constants.
    """


class constant:
    """A method decorator similar to @property but for use on class only classes. The
    decorated method is only called once per class. Subsequent calls simply return the
    stored value. This is useful for declaring a class level constant that is not
    actually created until it's used.

    Note that using @constant implies a classmethod. You don't need to also apply the
    classmethod decorator
    """

    def __init__(self, method):
        self.method = method
        self._values = {}

    def __set_name__(self, owner, name):
        if not isinstance(owner, OnlyMeta):
            raise TypeError(
                f"{type(self).__name__} can only be used with ClassOnly classes"
            )

    def __get__(self, instance, cls):
        if cls not in self._values:
            self._values[cls] = self.method(cls)
        return self._values[cls]
