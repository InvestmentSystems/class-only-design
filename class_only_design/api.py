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


