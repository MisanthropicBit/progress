#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Update a ProgressText in a thread while doing work in the main thread."""

from __future__ import print_function

__date__ = '2014-05-22'  # YYYY-MM-DD

import sys
sys.path.append('..')

import time
import random
import threading
import progress


def updater(event, progresstext):
    """"""
    while True:
        event.wait(0.5)

        if event.is_set():
            break

        progresstext.show()
        progresstext.update()

    progresstext.clear()


if __name__ == '__main__':
    text = progress.ProgressText('Searching{progress}', '...')

    # Create an event to signal the progress thread to stop
    stop_event = threading.Event()

    # Create and start the progress thread
    progress_thread = threading.Thread(target=updater, args=(stop_event, text))
    progress_thread.start()

    # Do some really important searching in the main thread
    for i in range(random.randint(5, 10)):
        time.sleep(random.randint(1, 2))

    # We are done searching, signal the progress thread and quit
    stop_event.set()
    progress_thread.join()

    print("Found {} entries in fictive database..."
          .format(random.randint(0, 6)))
