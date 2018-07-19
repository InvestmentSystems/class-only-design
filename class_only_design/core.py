# -*- coding: utf-8 -*-

"""
Functions intended to be used externally live here.
"""

import functools


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
        if cls._finished_decoration:
            raise TypeError("Class Only classes are immutable")
        return super().__setattr__(name, arg)


def class_only(cls):
    """
    Class only is a class decorator that disallows instantiation or state change on a class object.
    """
    # set updated to an empty iterable. By default wraps attempts to update __dict__, which isn't
    # valid on a class
    @functools.wraps(cls, updated=())
    class Only(cls, metaclass=OnlyMeta):
        _finished_decoration = False

        def __new__(*args, **kwargs):
            raise TypeError("Class Only classes cannot be instantiated")

    Only._finished_decoration = True
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
