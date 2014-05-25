# -*- coding: utf-8 -*-

"""Contains a single decorator function for inheriting docstrings."""

__date__ = '2014-05-25'  # YYYY-MM-DD

import sys
import functools


if sys.version_info[0] < 3:
    import types
    ClassType = types.ClassType

    def iteritems(d):
        return d.iteritems()
else:
    ClassType = type

    def iteritems(d):
        return d.items()


def inherit_docstrings(cls):
    """Class decorator for inheriting docstrings.

    Automatically inherits base class doc-strings if not present in the
    derived class.

    """
    @functools.wraps(cls)
    def _inherit_docstrings(cls):
        if not isinstance(cls, (type, ClassType)):
            raise RuntimeError("Type is not a class")

        for name, value in iteritems(vars(cls)):
            if isinstance(getattr(cls, name), types.MethodType):
                if not getattr(value, '__doc__', None):
                    for base in cls.__bases__:
                        basemethod = getattr(base, name, None)

                        if basemethod and getattr(base, '__doc__', None):
                            value.__doc__ = basemethod.__doc__

        return cls

    return _inherit_docstrings(cls)
