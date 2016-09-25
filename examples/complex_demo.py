#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""Demonstrates a complex ProgressBar."""

from __future__ import print_function

import time
import random
import progress
import progress.eta


def gen_random_update(mnsleep, mxsleep, mnvalue, mxvalue):
    """Generate a tuple of a random sleep period and update value."""
    while True:
        yield random.uniform(mnsleep, mxsleep),\
            random.randint(mnvalue, mxvalue)


if __name__ == '__main__':
    bar = progress.ProgressBar(fmt='[{progress}] {nominator}KB, eta: '
                                   '{minutes}m:{seconds}s',
                               width=35, char='#', head='',
                               etaobj=progress.eta.EMAETA())

    while not bar.done():
        bar.show()
        sleep, update = next(gen_random_update(1.0, 4.0, 5, 30))
        time.sleep(sleep)
        bar += update

    bar.show()
    print("\nDone...")
