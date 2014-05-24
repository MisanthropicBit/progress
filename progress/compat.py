# -*- coding: utf-8 -*-

"""Defines a set of Python 2/3 compatibility functions and imports."""

__date__ = '2014-05-17'  # YYYY-MM-DD

import progress


if progress._PY2:
    import types
    ClassType = types.ClassType

    def iteritems(d):
        """Return an iterator over the key-value pairs of a dictionary."""
        return d.iteritems()
else:
    ClassType = type

    def iteritems(d):
        """Return an iterator over the key-value pairs of a dictionary."""
        return d.items()
