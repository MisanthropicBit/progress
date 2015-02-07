#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstrates updating a ProgressBar from multiple worker threads."""

from __future__ import print_function

try:
    import Queue as queue  # Python 2
except ImportError:
    import queue  # Python 3

import time
import random
import threading
import progress

__date__ = '2015-02-07'  # YYYY-MM-DD


class WorkerThread(threading.Thread):

    """Generic worker thread."""

    def __init__(self, msgqueue):
        """Initialize the worker with a message queue."""
        super(WorkerThread, self).__init__()
        self._queue = msgqueue

        print("Starting worker thread '{}'...".format(self.name))

    def run(self):
        """Override Thread.run"""
        for i in range(10):
            time.sleep(random.randint(2, 5))
            self._queue.put(1)  # Block until thread can put the value


if __name__ == '__main__':
    # Create a message queue for communication in the main thread
    msgqueue = queue.Queue()
    worker_count = random.randint(3, 10)

    # Set the total amount of work for the ProgressBar
    total_work = worker_count * 10

    bar = progress.ProgressBar("Searching database: [{progress}] "
                               "{percentage: .0f}%",
                               max=total_work)

    print("Creating {} worker threads...".format(worker_count))

    # Create some random number of workers
    workers = [WorkerThread(msgqueue) for _ in range(worker_count)]

    # Start all workers
    for w in workers:
        w.start()

    # Display the progress bar
    bar.show()

    # Continue updating the progress bar while all workers are alive
    while any(w.is_alive() for w in workers):
        try:
            bar.update(msgqueue.get_nowait())
            bar.show()
        except queue.Empty:
            pass

    # Show completion and print a newline
    bar.show()
    print()

    # Join all workers
    for w in workers:
        w.join()

    print("All worker threads finished...")
