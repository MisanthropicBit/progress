"""Implements a simple moving average ETA class."""

import collections
import progress.decorators
from progress.eta.base import BaseETA

__date__ = '2015-04-15'  # YYYY-MM-DD


@progress.decorators.inherit_docstrings
class SMAETA(BaseETA):

    """Implements a (simple) moving average ETA."""

    def __init__(self, window):
        """Initialise the SMA ETA class with a window size.

        The window size determines the number of previous samples to consider
        when calculating the current moving average.

        """
        self.window = window
        self.reset()

    def update(self, time, value, maxvalue):
        self._maxvalue = maxvalue

        if self._history:
            dt, dv = (float(abs(i - j))
                      for i, j in zip(self._history, [time, value]))
        else:
            dt, dv = float(time), float(value)

        if dt > 0. and dv > 0.:
            speed = dv / dt

            if len(self._samples) == self.window:
                # Refrain from a doing the full summation
                last = self._samples[0]
                self._sma = self._sma - last / self.window +\
                    speed / self.window
            else:
                # Calculate mean as normal until we have enough samples
                self._sma = (sum(self._samples) + speed) /\
                    (len(self._samples) + 1)

            self._samples.append(speed)

        # Update ETA and history
        if self._sma > 0.:
            self._eta = (self._maxvalue - value) / self._sma

        self._history = [time, value]

    def get(self):
        return self.format_eta(self.eta) if self.eta else None

    def reset(self):
        self._eta = None
        self._sma = 0.
        self._maxvalue = 0.
        self._history = []
        self._samples = collections.deque(maxlen=self.window)

    @property
    def eta(self):
        return self._eta

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        if window < 1:
            raise ValueError("Window size must be at least 1")

        self._window = window
