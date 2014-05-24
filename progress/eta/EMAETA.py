"""A class implementing an exponentially moving average."""

__date__ = '2014-05-23'  # YYYY-MM-DD

import progress.decorators
from progress.eta.BaseETA import BaseETA


@progress.decorators.inherit_docstrings
class EMAETA(BaseETA):

    """Implements an exponentially moving average algorithm.

    Previous progress has an exponentially decreasing influence
    on the ETA and more recent progress has a bigger influence

    """

    def __init__(self, decay=0.1):
        """Decay controls how fast past values' effect decreases."""
        if decay < 0.0 or decay > 1.0:
            raise ValueError("Decay must be in range [0.0, 1.0]")

        self.decay = decay
        self.speed = 0.0
        self.ema = 0.0
        self.history = []

    def update(self, time, value, maxval):
        self.history.append((time, value))
        self.maxval = maxval
        lh = len(self.history)

        if lh > 1:
            dt = self.history[1][0] - self.history[0][0]
            ds = self.history[1][1] - self.history[0][1]
            speed = float(ds) / float(dt)
            self.ema = self.decay * speed + (1.0-self.decay) * self.ema
            self.history.pop(0)
        elif lh == 1:
            self.ema = self.history[0][1]
        else:
            self.ema = None

    def get(self):
        return self.format_eta(self.ema) if self.ema else None
