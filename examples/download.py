#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Using ProgressBar to simulate downloading some files."""

from __future__ import print_function

__date__ = '2014-10-04'  # YYYY-MM-DD

import time
import random
import progress


def download_file():
    """Simulate downloading a file."""
    time.sleep(random.uniform(0.1, 0.5))


if __name__ == '__main__':
    bar = progress.ProgressBar("Downloading '{}'... ")

    for i in range(5):
        bar.fmt = "Downloading '{}'... ".format('file' + str(i) + '.txt') +\
            "{nominator}%"

        while not bar.done():
            bar.autoupdate(1)
            download_file()

        print()

    print("Done...")
