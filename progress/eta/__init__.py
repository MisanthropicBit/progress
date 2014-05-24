"""Contains all ETA object classes.

Defines a set of estimated time of arrival classes as well as a base class
to allow user-defined ETA classes

"""

__date__ = '2014-02-18'  # YYYY-MM-DD

from progress.eta.BaseETA import BaseETA
from progress.eta.SimpleETA import SimpleETA
# from progress.eta.SMAETA import SMAETA
from progress.eta.EMAETA import EMAETA
