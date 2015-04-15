"""Contains all ETA object classes.

Defines a set of estimated time of arrival classes as well as a base class
to allow user-defined ETA classes

"""


from progress.eta.base import BaseETA
from progress.eta.simple import SimpleETA
from progress.eta.sma import SMAETA
from progress.eta.ema import EMAETA

__date__ = '2015-04-14'  # YYYY-MM-DD
