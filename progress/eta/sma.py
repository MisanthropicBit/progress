"""Implements a moving average ETA class."""

import progress.decorators
from progress.eta.base import BaseETA

__date__ = '2015-03-18'  # YYYY-MM-DD


@progress.decorators.inherit_docstrings
class SMAETA(BaseETA):

    """Implements a (simple) moving average ETA."""

    def __init__(self):
        pass
