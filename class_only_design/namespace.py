import functools

from class_only_design import core


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


def _is_internal(name):
    """Return true if the given name is internal to the class_only_design library. Currently we
    check for __dunder__ and _sunder_names
    """
    return _is_dunder(name) or _is_sunder(name)


class MetaNamespace(core.OnlyMeta):
    def __iter__(cls):
        for k, v in vars(cls.__mro__[1]).items():
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
        _finished_initialization = False

        def __new__(*args, **kwargs):
            raise TypeError("Class Only classes cannot be instantiated")

    NS._finished_initialization = True
    return NS
