"""Implements a simple ETA calculation."""

import collections
import progress.decorators
from progress.eta.base import BaseETA

__date__ = '2015-03-18'  # YYYY-MM-DD


@progress.decorators.inherit_docstrings
class SimpleETA(BaseETA):

    """Implements a simple ETA calculation routine.

    It considers only the difference between the current progress
    and the previous one. This is the default used in the ProgressBar
    class if the user does not provide one.

    """

    def __init__(self):
        self._deque = collections.deque()
        self.reset()

    def update(self, time, value, maxval):
        self._deque.append(tuple(time, value))
        self._maxval = _maxval

        if len(self._deque) > 1:
            # Compute differences in speed and
            # time between the last two updates
            dt = float(self._deque[-1][0]) - float(self._deque[-2][0])
            dv = self._deque[-1][1] - self._deque[-2][1]

            speed = dv / dt
            self._deque.popleft()

            if speed != 0.0:
                self.eta = float(self._maxval - self._deque[1][1]) / speed
            else:
                self.eta = None

    def get(self):
        return self.format_eta(self.eta)

    def reset(self):
        self._deque.clear()
        self.eta = 0
