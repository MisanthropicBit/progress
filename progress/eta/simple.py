"""Implements a simple ETA calculation."""

import progress.decorators
from progress.eta.base import BaseETA

__date__ = '2015-04-13'  # YYYY-MM-DD


@progress.decorators.inherit_docstrings
class SimpleETA(BaseETA):

    """Implements a simple ETA calculation routine.

    It considers only the difference between the current progress
    and the previous one. This is the default used in the ProgressBar
    class if the user does not provide one.

    """

    def __init__(self):
        self.reset()

    def update(self, time, value, maxvalue):
        self._maxvalue = maxvalue

        if self._history:
            dt, dv = (float(abs(i - j))
                      for i, j in zip(self._history, [time, value]))
        else:
            dt, dv = time, value

        if dt > 0. and dv > 0.:
            self._eta = float(self._maxvalue - value) / (dv / dt)

        # Update history
        self._history = [time, value]

    def get(self):
        return self.format_eta(self.eta)

    def reset(self):
        self._history = []
        self._eta = 0
        self._maxvalue = 0

    @property
    def eta(self):
        return self._eta
