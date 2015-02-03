# -*- coding: utf-8 -*-

"""ProgressText class."""

__date__ = '2015-02-03'  # YYYY-MM-DD

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


# Ensure compatibility with both Python 2.x/3.x lazy range functions
try:
    irange = xrange
except NameError:
    irange = range


class ProgressText(object):

    """Represents updatable progress text for Python 2.6+."""

    _VALID_FMT = 'progress'

    def __init__(self, fmt, progress, autoreset=False, include_empty=False,
                 target=sys.stdout):
        """Initialize with static text.

        E.g. 'Searching' and a list of postfixes. If autoreset
        is set to True, clears each postfix on each update, otherwise
        they're appended. If include_empty is True and autoreset is False, then
        include the emtpy string when progressing.

        """
        self._check_format(fmt)

        self._fmt = fmt
        self._progress = progress
        self._autoreset = autoreset
        self.include_empty = include_empty
        self.target = target
        self._fmtdict = {}
        self._txt = fmt
        self._lastlen = 0
        self.reset()

    def update(self):
        """Update the progress text."""
        self._fmtdict[ProgressText._VALID_FMT] = next(self._cycle)

    def clear(self):
        """Remove the progress text from the output stream."""
        mv_cursor = '\r' * self._lastlen

        self._target.write(mv_cursor)
        self._target.write(' ' * self._lastlen)
        self._target.write(mv_cursor)

    def reset(self):
        """Reset the progress text."""
        if self.autoreset:
            self._cycle = itertools.cycle(self._progress)
        else:
            self._cycle = itertools.cycle(self._progress[:end]
                                          for end in
                                          irange(0 if self.include_empty
                                                 else 1,
                                                 len(self._progress) + 1))

        self.update()

    def show(self, *args, **kwargs):
        """Write the progress text to the console."""
        if args or kwargs:
            tempdict = dict(**self._fmtdict)

            if kwargs:
                if any(kw in self._fmtdict for kw in kwargs):
                    raise ValueError("kwargs cannot override internal "
                                     "format keys")
                tempdict.update(kwargs)

            self._txt = self._fmt.format(*args, **tempdict)
        else:
            self._txt = self._fmt.format(**self._fmtdict)

        self.clear()
        self._target.write(self._txt)
        self._target.flush()  # Needed for Python 3.x
        self._lastlen = len(self._txt)

    def autoupdate(self, *args, **kwargs):
        """Clear, update and show the progress text.

        Essentially, a short-hand way of doing:
            text.clear()
            text.update()
            text.show()

        """
        self.clear()
        self.show(*args, **kwargs)
        self.update()

    def _check_format(self, fmt):
        """Check that a given format is valid."""
        if not fmt:
            raise ValueError("Expected a non-empty format string")

        count = 0

        for _, name, _, _ in string.Formatter().parse(fmt):
            if name == ProgressText._VALID_FMT:
                count += 1
                if count > 1:
                    raise ValueError("'{0}' appears more than once"
                                     .format(name))

    @property
    def value(self):
        """Return the current progress char(s)."""
        return self._fmtdict[ProgressText._VALID_FMT]

    @property
    def autoreset(self):
        """Set the autoreset flag.

        The progress text's internal state is reset if this is
        changed.

        """
        return self._autoreset

    @autoreset.setter
    def autoreset(self, value):
        self._autoreset = value
        self.reset()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, t):
        if t not in (sys.stdout, sys.stderr):
            raise ValueError("Valid targets are either sys.stdout or "
                             "sys.stderr")

        self._target = t

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.reset()

    @property
    def format(self):
        return self._fmt

    @format.setter
    def format(self, fmt):
        self._check_format(fmt)
        self._fmt = fmt

    def __str__(self):
        """Return the string representation as used by show()."""
        return self._fmt.format(**self._fmtdict)

    def __repr__(self):
        """Return the same string representation as __str()__."""
        return "<{} at 0x{}>".format(self.__class__.__name__, id(self))

    def __len__(self):
        """Return the current length of the progress in characters."""
        return len(self.__str__())
