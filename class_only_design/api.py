import functools

from class_only_design.meta import OnlyMeta
from class_only_design.meta import MetaNamespace
from class_only_design import util


def class_only(cls):
    """
    Class only is a class decorator that disallows instantiation or state change on a class object.
    """
    classdict = {k: v for k, v in cls.__dict__.items()}
    new = OnlyMeta(cls.__name__, cls.__bases__, classdict)

    return new


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

    classdict = {k: v for k, v in cls.__dict__.items()}
    classdict["_initializing_"] = True
    new = MetaNamespace(cls.__name__, cls.__bases__, classdict)
    new.nameof = util.KeyGetter(new)
    del new._initializing_

    return new
