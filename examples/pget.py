#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""A silly (and possibly very immature) demonstration of ProgressBar usage."""

__date__ = '2014-05-17'  # YYYY-MM-DD

import time
import random
import progress
import progress.eta


def main():
    pbar = progress.ProgressBar(fmt='[{progress}] {percentage}%'
                                    '{hours}:{minutes}',
                                width=40, head='D',
                                etaobj=progress.eta.SMAETA())

    while True:
        time.sleep(random.randint(0, 2))
        pbar.update(random.randint(20, 80))
        pbar.show()

        if pbar.done():
            pbar.show()
            break
