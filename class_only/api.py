# -*- coding: utf-8 -*-

"""
Functions intended to be used externally live here.
"""

import functools


class OnlyMeta(type):
    def __setattr__(cls, name, arg):
        if cls._finished_decoration:
            raise TypeError("Class Only classes are immutable")
        return super().__setattr__(name, arg)


def class_only(cls):
    """
    Class only is a class decorator that disallows instantiation or state change on a class object.
    """
    # set updated to an empty iterable. By default it attempts to update __dict__, which isn't
    # valid on a class
    @functools.wraps(cls, updated=())
    class Only(cls, metaclass=OnlyMeta):
        _finished_decoration = False

        def __new__(*args, **kwargs):
            raise TypeError("Class Only classes cannot be instantiated")

    Only._finished_decoration = True
    return Only
