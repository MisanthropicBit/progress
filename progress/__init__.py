# -*- coding: utf-8 -*-

"""progress v1.3.0.

A cross-platform Python 2/3 module for command line updatable progress
trackers. The following classes are made available:

Name          Description                        Example
ProgressBar   Flexible progress bar   '[===>        ] 33.3%'
ProgressText  Flexible progress text  'Searching...'

"""

import sys
from progress.ProgressBar import ProgressBar
from progress.ProgressText import ProgressText

__author__ = 'Alexander Bock'
__version__ = '1.3.0'
__date__ = '2015-05-19'  # YYYY-MM-DD


_DEBUG_MODE = False

if _DEBUG_MODE:  # pragma: no cover
    print("Python " + ".".join(map(str, sys.version_info[:3])))
