"""A class implementing an exponentially moving average."""

import progress.decorators
from progress.eta.base import BaseETA

__date__ = '2015-04-13'  # YYYY-MM-DD


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
        self._maxvalue = maxvalue

        if self._history:
            # Compute the differences between time and values
            dt, dv = (float(abs(i - j))
                      for i, j in zip(self._history, [time, value]))
        else:
            dt, dv = float(time), float(value)

        if dt > 0. and dv > 0.:
            # Update the exponentially moving average
            self._ema = self.decay * (dv / dt) + (1. - self.decay) * self._ema
        else:
            self._ema = 0.

        # Update ETA and history
        if self._ema > 0.:
            self._eta = (self._maxvalue - value) / self._ema

        self._history = [time, value]

    def get(self):
        return self.format_eta(self.eta) if self.eta else None

    def reset(self):
        self._eta = None
        self._ema = 0.
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
