#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""A silly (and possibly very immature) demonstration of ProgressBar usage."""

from __future__ import print_function

import time
import random
import progress
import progress.eta

__date__ = '2015-02-07'  # YYYY-MM-DD


if __name__ == '__main__':
    pbar = progress.ProgressBar(fmt='[{progress}] {percentage:.2f}% '
                                    '{hours}:{minutes}',
                                width=40, head='D',
                                etaobj=progress.eta.EMAETA())

    while True:
        pbar.show()
        time.sleep(random.randint(1, 2))
        pbar.update(random.randint(10, 40))

        if pbar.done():
            pbar.show()
            print()
            break
