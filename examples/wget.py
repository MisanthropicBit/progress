#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""An example that mimicks the progress bar of wget."""

from __future__ import print_function

import time
import random
import progress


if __name__ == '__main__':
    fmt = '{percentage:.0f}% [{progress}] eta {minutes:.2f}m {seconds:.2f}s'
    bar = progress.ProgressBar(fmt, width=45, max=73945,
                               etaobj=progress.eta.EMAETA())

    while True:
        bar.show()
        time.sleep(random.randint(1, 2))
        bar.update(random.randint(8245, 9245))

        if bar.done():
            bar.show()
            print()
            break
