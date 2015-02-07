"""Contains all ETA object classes.

Defines a set of estimated time of arrival classes as well as a base class
to allow user-defined ETA classes

"""


from progress.eta.BaseETA import BaseETA
from progress.eta.SimpleETA import SimpleETA
# from progress.eta.SMAETA import SMAETA
from progress.eta.EMAETA import EMAETA

__date__ = '2015-02-07'  # YYYY-MM-DD
