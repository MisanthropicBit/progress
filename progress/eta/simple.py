"""Implements a simple ETA calculation."""

import progress.decorators
from progress.eta.base import BaseETA


@progress.decorators.inherit_docstrings
class SimpleETA(BaseETA):

    """Implements a simple ETA calculation routine.

    It considers only the difference between the current progress
    and the previous one. This is the default used in the ProgressBar
    class if the user does not provide one.

    """

    def __init__(self):
        self.reset()

    def update(self, time, value, max_value):
        if self._history:
            dt, dv = (float(abs(i - j))
                      for i, j in zip(self._history, [time, value]))
        else:
            dt, dv = time, value

        if dt > 0. and dv > 0.:
            self._eta = float(max_value - value) / (dv / dt)

        self._history = [time, value]

    def get(self):
        return self.format_eta(self.eta)

    def reset(self):
        self._history = []
        self._eta = 0

    @property
    def eta(self):
        return self._eta
