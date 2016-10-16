# -*- coding: utf-8 -*-

"""ProgressBar class."""


import sys
import time
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
    _VALID_FMTS = ['progress', 'percentage', 'nominator', 'denominator']\
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
        if int(width) <= 0:
            raise ValueError("Width must be greater than zero")

        c, h = len(char), len(head)

        if c != 1:
            raise ValueError("char and head must be of length 1")

        if c > width or h > width or c + h > width:
            raise ValueError("Character lengths or combined length must be "
                             "less than progress bar width")

        self._progchar = fill * width
        self._fmtdict = dict(zip(ProgressBar._VALID_FMTS,
                                 [self._progchar, 0.0, 0, max, 0, 0, 0]))

        # Check the format is valid
        self._check_format(fmt)

        self._etaobj = None

        if etaobj is None:
            if self._has_eta:
                self._etaobj = progress.eta.SimpleETA()
        else:
            if not self._has_eta:
                raise ValueError("Specified etaobj, but missing eta format in "
                                 "format string")

            if not isinstance(etaobj, progress.eta.BaseETA):
                raise TypeError("ETA object must derive from the "
                                "progress.eta.BaseETA class")

            self._etaobj = etaobj

        self._width = width
        self._char = char
        self._head = head
        self._fill = fill
        self._min = min
        self._max = max
        self._fmt = fmt
        self._target = target
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

        if value > 0:
            self._value += value
            # Clamp to [mn, mx]
            self.value = max(self.min, min(self.value, self.max))

        v = float(self.value - self.min) / float(self.max - self.min)
        self._percentage = v

        # Set progress string
        if not self.done():
            lh = len(self.head)

            self._progchar = self.char * ((int(v * self.width) - lh) //
                                          len(self.char)) + self.head
            self._progchar += self.fill * (self.width - len(self._progchar))
        else:
            self._progchar = self.char * (self.width - 1) +\
                (self.char if not self.head else self.head)

        self._fmtdict.update(zip([ProgressBar._PROGRESS,
                                  ProgressBar._PERCENTAGE,
                                  ProgressBar._NOMINATOR],
                                 [self._progchar,
                                  self._percentage * 100.0,
                                  self._value]))

    def update(self, value):
        """Update the progress bar with value."""
        # Update and format ETA if needed
        if self._has_eta:
            self._etaobj.update(self._timer(), self._value, self.max)
            res = self._etaobj.get()

            if res is not None:
                if type(res) not in (tuple, list):
                    raise ValueError("Expected a tuple or list of three "
                                     "elements from ETA object, not "
                                     "'{0}'".format(type(res).__name__))

                if len(res) != 3:
                    raise ValueError("Expected exactly three elements from "
                                     "ETA object, not '{0}'"
                                     .format(type(res).__name__))

                self._fmtdict.update(zip(ProgressBar._VALID_ETA, res))

        self._update(value)

    def clear(self):
        """Remove the progress bar from the output stream."""
        self._target.write('\r' + ' ' * self._lastlen + '\r')

    def reset(self):
        """Reset the progress bar."""
        self.value = self.min

        if self._etaobj:
            self._etaobj.reset()

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
        self._target.write(tmp)
        self._target.flush()  # Needed for Python 3.x
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

    def _check_format(self, fmt):
        """Check that a given format is valid."""
        if not fmt:
            raise ValueError("Expected a non-empty format string")

        fmt_count = dict.fromkeys(ProgressBar._VALID_FMTS, 0)
        self._has_eta = False

        for _, name, _, _ in string.Formatter().parse(fmt):
            if name in ProgressBar._VALID_ETA:
                self._fmtdict[name] = 0
                self._has_eta = True
            elif name in ProgressBar._VALID_FMTS:
                fmt_count[name] += 1

                if fmt_count[name] > 1:
                    raise ValueError("Format string '{0}' appears more "
                                     "than once".format(name))

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if width < 1:
            raise ValueError("Width must be at least 1 character")

        self._width = width
        self._update(0)

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, char):
        if len(char) != 1:
            raise ValueError("char must be one character")

        self._char = char
        self._update(0)

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        if len(head) != 1:
            raise ValueError("head must be one character")

        self._head = head
        self._update(0)

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, fill):
        if len(fill) != 1:
            raise ValueError("fill must be one character")

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
        elif self._value >= value:
            self._value = value
            self.update(0)

    @property
    def percent(self):
        return self._percentage

    @percent.setter
    def percent(self, percent):
        # Percentage will be set in self._update
        self._value = self.min + percent * (self.max - self.min)
        self._update(0)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, min):
        if min >= self.max:
            raise ValueError("min must less than max ({0})".format(self.max))

        self._min = min
        self._update(0)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, max):
        if max <= self.min:
            raise ValueError("max must greater than min ({0})"
                             .format(self.min))

        self._max = max
        self._update(0)

    @property
    def format(self):
        return self._fmt

    @format.setter
    def format(self, fmt):
        self._check_format(fmt)
        self._fmt = fmt

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, t):
        if t not in (sys.stdout, sys.stderr):
            raise ValueError("Valid targets are either sys.stdout or "
                             "sys.stderr")

        self._target = t

    def __str__(self):
        """Return the string representation as used by show()."""
        return self._fmt.format(**self._fmtdict)

    def __repr__(self):
        """Return the same string representation as __str()__."""
        return "ProgressBar(format={0!r}, value={1!r})".format(self.format,
                                                               self.value)

    def __iadd__(self, value):
        """Update the progress bar with value."""
        self.update(value)
        return self

    def __len__(self):
        """Return the current length of the progress in characters."""
        return len(str(self))
