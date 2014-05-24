"""Implements a simple ETA calculation.

Considers the difference in current and immediate
past value

"""

__date__ = '2014-02-19'  # YYYY-MM-DD

import progress.decorators
from progress.eta.BaseETA import BaseETA


@progress.decorators.inherit_docstrings
class SimpleETA(BaseETA):

    """Implements a simple ETA calculation routine.

    It considers only the difference between the current progress
    and the previous one. This is the default used in the ProgressBar
    class if the user does not provide one

    """

    def __init__(self):
        self.history = []
        self.eta = 0.0

    def update(self, time, value, maxval):
        self.history.append((time, value))
        self.maxval = maxval

        if len(self.history) > 1:
            dt = self.history[1][0] - self.history[0][0]
            ds = self.history[1][1] - self.history[0][1]
            speed = float(ds) / float(dt)
            self.history.pop(0)

            if speed != 0.0:
                self.eta = float(self.maxval - self.history[0][1]) / speed
            else:
                self.eta = -1

    def get(self):
        return self.format_eta(self.eta)
