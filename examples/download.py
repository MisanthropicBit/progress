#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Using ProgressBar to simulate downloading some files."""

from __future__ import print_function

import time
import random
import progress


def download_file():
    """Simulate downloading a file."""
    time.sleep(random.uniform(0.1, 0.2))


if __name__ == '__main__':
    bar = progress.ProgressBar("Downloading '{}'... ")

    for i in range(1, 4):
        bar.reset()
        bar.format = "Downloading '{}'... ".format('file' + str(i) + '.txt') +\
            "{nominator}%"

        while not bar.done():
            bar.autoupdate(random.randint(1, 5))
            download_file()

        print()

    print("Done...")
