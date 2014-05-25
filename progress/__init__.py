# -*- coding: utf-8 -*-

"""progress v1.1.0.

A cross-platform Python 2/3 module for command line updatable progress
trackers. The following classes are made available:

Name          Description                        Example
ProgressBar   Flexible progress bar   '[===>        ] 33.3%'
ProgressText  Flexible progress text  'Searching...'

"""

__author__ = 'Alexander Bock'
__version__ = '1.1.0'
__date__ = '2014-05-25'  # YYYY-MM-DD

import sys

_DEBUG_MODE = False  # Refrain from using __debug__

if _DEBUG_MODE:
    print("Python " + ".".join(map(str, sys.version_info[:3])))


from progress.ProgressBar import ProgressBar
from progress.ProgressText import ProgressText
