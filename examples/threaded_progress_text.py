#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Update a ProgressText in a thread while doing work in the main thread."""

from __future__ import print_function

__date__ = '2014-06-16'  # YYYY-MM-DD

import sys
sys.path.append('..')

import time
import random
import threading
import progress


def updater(event, progresstext):
    """Updater function to be called by threads."""
    while True:
        event.wait(0.5)

        if event.is_set():
            break

        progresstext.autoupdate()

    progresstext.clear()


if __name__ == '__main__':
    text = progress.ProgressText('Searching{progress}', '...',
                                 include_empty=True)

    # Create an event to signal the progress thread to stop
    stop_event = threading.Event()

    # Show the progress text, then create and start the progress thread
    text.show()
    progress_thread = threading.Thread(target=updater, args=(stop_event, text))
    progress_thread.start()

    # Do some really important searching in the main thread
    for i in range(random.randint(5, 10)):
        time.sleep(random.randint(1, 2))

    # We are done searching, signal the progress thread and quit
    stop_event.set()
    progress_thread.join()

    print("Found {} entrie(s) in fictive database..."
          .format(random.randint(0, 6)))
