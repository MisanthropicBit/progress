"""A class implementing an exponentially moving average."""

import collections
import progress.decorators
from progress.eta.base import BaseETA

__date__ = '2015-03-18'  # YYYY-MM-DD


@progress.decorators.inherit_docstrings
class EMAETA(BaseETA):

    """Implements an exponentially moving average algorithm.

    Previous progress has an exponentially decreasing influence
    on the ETA and more recent progress has a bigger influence

    """

    def __init__(self, decay=0.1):
        """Decay controls how fast past values' effect decreases."""
        self.decay = decay
        self.reset()

    def update(self, time, value, maxval):
        if self._ema is None:
            self._ema = float(value) / float(time)
        else:
            # Compute the differences between time and values
            dt = time - self._prev_values[0]
            dv = value - self._prev_values[1]

            # Update the exponentially moving average
            self._ema = self.decay * (float(dv) / float(dt)) +\
                (1. - self.decay) * self._ema

            # Update the previous values with the current
            self._prev_values = tuple(time, value)

        self.history.append((time, value))
        self.maxval = maxval
        lh = len(self.history)

        if lh > 1:
            dt = self.history[1][0] - self.history[0][0]
            ds = self.history[1][1] - self.history[0][1]
            speed = float(ds) / float(dt)
            self.ema = self.decay * speed + (1.0 - self.decay) * self.ema
            self.history.pop(0)
        elif lh == 1:
            self.ema = self.history[0][1]
        else:
            self.ema = None

    def get(self):
        return self.format_eta(self._ema) if self._ema else None

    def reset(self):
        self.speed = 0.
        self.ema = 0.
        self.history = []

    @property
    def decay(self):
        return self._decay

    @decay.setter
    def decay(self, decay):
        if decay < 0.0 or decay > 1.0:
            raise ValueError("Decay must be in range [0.0, 1.0]")

        self._decay = decay
