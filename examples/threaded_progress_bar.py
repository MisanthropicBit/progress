#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstrates updating a ProgressBar from multiple worker threads."""

from __future__ import print_function

__date__ = '2014-05-21'  # YYYY-MM-DD

try:
    import Queue as queue  # Python 2
except ImportError:
    import queue  # Python 3

import time
import random
import threading
import progress


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
    msgqueue = queue.queue()
    worker_count = random.randint(3, 10)

    # Set the total amount of work for the ProgressBar
    total_work = worker_count * 10

    bar = progress.ProgressBar("Searching database: [{progress}] "
                               "{percentage: .f}",
                               mx=total_work)

    print("Creating {} worker threads...".format(worker_count))

    # Create some random number of workers
    workers = [WorkerThread(msgqueue) for _ in range(worker_count)]

    # Start all workers
    map(lambda x: x.start(), workers)

    # Continue updating the progress bar while all workers are alive
    while any(lambda x: x.is_alive(), workers):
        try:
            bar.update(msgqueue.get_nowait())
        except queue.Empty:
            pass

    # Join all workers
    map(lambda x: x.join(), workers)

    print("All worker threads finished...")
