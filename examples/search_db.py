#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""Simple usage of ProgressText."""

__date__ = '2014-06-16'  # YYYY-MM-DD

import time
import progress


def update_progtxt(progress_text):
    while True:
        progress_text.clear()
        progress_text.show()

if __name__ == '__main__':
    text = progress.ProgressText('Searching {progress}', '/-\\|',
                                 autoreset=True)

    for i in range(10):
        text.autoupdate()
        time.sleep(0.3)

    text.clear()
