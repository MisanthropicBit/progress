# -*- coding: utf-8 -*-

"""ProgressBar class."""

__date__ = '2014-06-12'  # YYYY-MM-DD

import sys
import time
import copy
import string
import progress
import progress.eta


class ProgressBar(object):

    """A flexible progress bar for Python 2.6+."""

    # Valid format strings
    _PROGRESS = 'progress'
    _PERCENTAGE = 'percentage'
    _NOMINATOR = 'nominator'
    _DENOMINATOR = 'denominator'
    _VALID_ETA = ['hours', 'minutes', 'seconds']
    _VALID_FMTS = ['progress', 'percentage', 'nominator', 'denominator'] \
        + _VALID_ETA

    def __init__(self, fmt, width=20, char='=', head='>', fill=' ',
                 min=0, max=100, target=sys.stderr, etaobj=None):
        """Initialize the progress bar with keyword arguments.

        width     The character width of the progress bar
        char      The character that fills progress bar
        head      The lead character
        fill      Character for the remaining space
        min       Minimum/starting value
        max       Maximum/end value
        fmt       The format used to print on each update
        target    The target stream, defaults to sys.stderr
        etaobj    A subclass of progress.eta.ETA

        """
        # Do a ton of error checking to ensure a valid format and parameters
        if not fmt:
            raise ValueError("Expected a non-empty format string")

        if int(width) <= 0:
            raise ValueError("Width must be greater than zero")

        c, h = len(char), len(head)

        if c != 1:
            raise ValueError("char and head must be of length 1")

        if c > width or h > width or c + h > width:
            raise ValueError("Character lengths or combined length must be "
                             "less than progress bar width")

        fmt_count = dict.fromkeys(ProgressBar._VALID_FMTS, 0)
        self.has_eta = False
        self._progchar = fill * width
        self._fmtdict = dict(zip(ProgressBar._VALID_FMTS,
                                 [self._progchar, 0.0, 0, max, 0, 0, 0]))

        for _, name, _, _ in string.Formatter().parse(fmt):
            if name in ProgressBar._VALID_ETA:
                self._fmtdict[name] = 0
                self.has_eta = True
            elif name in ProgressBar._VALID_FMTS:
                fmt_count[name] += 1

                if fmt_count[name] > 1:
                    raise ValueError("Format string '{0}' appears more "
                                     "than once".format(name))

        if etaobj is None:
            if self.has_eta:
                self.etaobj = progress.eta.SimpleETA()
        else:
            if not self.has_eta:
                raise ValueError("Specified etaobj, but missing eta format in "
                                 "format string")

            if not isinstance(etaobj, progress.eta.BaseETA):
                raise TypeError("ETA object must derive from the "
                                "progress.eta.BaseETA class")

            self.etaobj = etaobj

        self._width = width
        self._char = char
        self._head = head
        self._fill = fill
        self._min = min
        self._max = max
        self._fmt = fmt
        self.target = target
        self._value = min
        self._percentage = 0.0
        self._bdels = 0
        self._timer = time.clock if sys.platform.startswith('win')\
            else time.time
        self._lastlen = 0

    def _update(self, value):
        """Internal method for updating the ProgressBar's state."""
        if value < 0:
            raise ValueError("Cannot update progress bar with"
                             "a negative value")

        if value != 0:
            self._value = self._value + value
            # Clamp to [mn, mx]
            self._value = max(self.min, min(self._value, self.max))

        v = float(self._value - self.min) / float(self.max - self.min)
        self._percentage = v

        # Set progress string
        if not self.done():
            lh = len(self._head)

            self._progchar = self._char * ((int(v * self._width) - lh) //
                                           len(self._char))
            self._progchar += self._head + (self._fill * (self._width -
                                            (len(self._progchar) + lh)))
        else:
            self._progchar = self._char * (self._width - 1) +\
                (self._char if not self._head else self._head)

        self._fmtdict.update(zip([ProgressBar._PROGRESS,
                                 ProgressBar._PERCENTAGE,
                                 ProgressBar._NOMINATOR],
                                 [self._progchar,
                                  self._percentage * 100.0,
                                  self._value]))

    def update(self, value):
        """Update the progress bar with value."""
        # Update and format ETA if needed
        if self.has_eta:
            self.etaobj.update(self._timer(), self._value, self.max)
            res = self.etaobj.get()

            if res is not None:
                if type(res) not in (tuple, list):
                    raise ValueError("Expected a tuple of three elements "
                                     "from ETA object")

                if len(res) != 3:
                    raise ValueError("Unexpected type '{0}' returned from ETA "
                                     "object".format(type(res).__name__))

                self._fmtdict.update(zip(ProgressBar._VALID_ETA, res))

        self._update(value)

    def clear(self):
        """Remove the progress bar from the output stream."""
        mv_cursor = '\r' * self._lastlen

        self.target.write(mv_cursor)
        self.target.write(' ' * self._lastlen)
        self.target.write(mv_cursor)

    def reset(self):
        """Reset the progress bar."""
        self.value = self.min

    def done(self):
        """Return True if the progress bar has completed."""
        return self._value == self.max

    def show(self, *args, **kwargs):
        """Print the progress bar.

        args and kwargs can contain userdata

        """
        tempdict = dict(**self._fmtdict)

        if kwargs:
            if any(kw in self._fmtdict for kw in kwargs):
                raise ValueError("kwargs cannot override internal format keys")

            tempdict.update(kwargs)

        self.clear()
        tmp = self._fmt.format(*args, **tempdict)
        self.target.write(tmp)
        self._lastlen = len(tmp)

    def autoupdate(self, value, *args, **kwargs):
        """Clear the progress bar, update it with value and show it.

        Essentially, a short-hand way of doing:
            bar.clear()
            bar.update(value)
            bar.show()

        """
        self.clear()
        self.update(value)
        self.show(*args, **kwargs)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._update(0)

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, char):
        self._char = char
        self._update(0)

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        self._head = head
        self._update(0)

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, fill):
        self._fill = fill
        self._update(0)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = max(self.min, min(self.max, value))

        if self._value < value:
            self.update(value - self._value)
        elif self._value > value:
            self._value = value
            self.update(0)

    @property
    def percent(self):
        return self._percentage

    @percent.setter
    def percent(self, percent):
        self._percentage = percent
        self._update(0)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, min):
        self._min = min
        self._update(0)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, max):
        self._max = max
        self._update(0)

    def __str__(self):
        """Return the string representation as used by show()."""
        return self._fmt.format(**self._fmtdict)

    def __repr__(self):
        """Return the same string representation as __str()__."""
        return "<{} at 0x{}>".format(self.__class__.__name__, id(self))

    def __iadd__(self, value):
        """Update the progress bar with value."""
        self.update(value)
        return self

    def __len__(self):
        """Return the current length of the progress in characters."""
        return self._value
