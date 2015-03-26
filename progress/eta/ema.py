"""A class implementing an exponentially moving average."""

import progress.decorators
from progress.eta.base import BaseETA

__date__ = '2015-03-26'  # YYYY-MM-DD


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

    def update(self, time, value, maxvalue):
        if self._history:
            # Compute the differences between time and values
            dt, dv = (float(abs(i-j))
                      for i, j in zip(self._history, [time, value]))

            # Update the exponentially moving average
            self._ema = self.decay * (float(dv) / float(dt)) +\
                (1. - self.decay) * self._ema
        else:
            self._ema = float(value) / float(time)

        # Update ETA and history
        if self._ema > 0.:
            self._eta = (maxvalue - value) / self._ema

        self._history = [time, value]

    def get(self):
        return self.format_eta(self._ema) if self._ema else None

    def reset(self):
        self._eta = None
        self._ema = None
        self._maxvalue = 0.
        self._history = []

    @property
    def eta(self):
        return self._eta

    @property
    def decay(self):
        return self._decay

    @decay.setter
    def decay(self, decay):
        if decay < 0.0 or decay > 1.0:
            raise ValueError("Decay must be in range [0.0, 1.0]")

        self._decay = decay
