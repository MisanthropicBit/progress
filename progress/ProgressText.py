# -*- coding: utf-8 -*-

"""ProgressText class."""

__date__ = '2014-05-22'  # YYYY-MM-DD

import sys
import string
import itertools


# Ensure compatibility with both Python 2.x/3.x next functions
try:
    next
except NameError:
    def _next(it):
        return it.next()

    next = _next


# Ensure compatibility with both Python 2.x/3.x (x)range functions
try:
    irange = xrange
except NameError:
    irange = range


class ProgressText(object):

    """Represents updatable progress text for Python 2.6+."""

    _VALID_FMT = 'progress'

    def __init__(self, fmt, progress, autoreset=False, target=sys.stdout):
        """Initialize with static text.

        E.g. 'Searching' and a list of postfixes. If autoreset
        is set to True, clears each postfix on each update, otherwise
        they're appended.

        """
        if not fmt:
            raise ValueError("Expected a non-empty format string")

        formatter = string.Formatter()
        count = 0

        for _, name, _, _ in formatter.parse(fmt):
            if name == ProgressText._VALID_FMT:
                count += 1
                if count > 1:
                    raise ValueError("'{0}' appears more than once"
                                     .format(name))

        self.fmt = fmt
        self.progress = progress
        self.autoreset = autoreset
        self.target = target
        self._fmtdict = {}
        self._txt = fmt
        self._lastlen = 0
        self.reset()

    def update(self):
        """Update the progress text."""
        self._fmtdict[ProgressText._VALID_FMT] = next(self._cycle)
        self._txt = self.fmt.format(**self._fmtdict)

    def clear(self):
        """Remove the progress text from the output stream."""
        mv_cursor = '\r' * self._lastlen

        self.target.write(mv_cursor)
        self.target.write(' ' * self._lastlen)
        self.target.write(mv_cursor)

    def reset(self):
        """Reset the progress text."""
        if self.autoreset:
            self._cycle = itertools.cycle(self.progress)
        else:
            self._cycle = itertools.cycle(self.progress[:end]
                                          for end in
                                          irange(0, len(self.progress)+1))

        self.update()

    def show(self):
        """Write the progress text to the console."""
        self.clear()
        self.target.write(self._txt)
        self.target.flush()
        self._lastlen = len(self._txt)
