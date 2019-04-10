import weakref

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
        # Hold a weakref to cls to avoid a circular reference
        self._cls_ = weakref.proxy(cls)

    def __getattr__(self, attr):
        # Call getattr, so that an exception is raised as normal if the attr doesn't exist
        getattr(self._cls_, attr)
        return attr

    def __dir__(self):
        return sorted(vars(self._cls_))


class NamespaceLoader(dict):
    def __setitem__(self, k, v):
        if v is constants.autoname:
            return super().__setitem__(k, k)
        return super().__setitem__(k, v)
