#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""Using ProgressText in a separate thread while searching a fake database."""

import time
import random
import threading
import progress


def update_progtxt(ptxt):
    ptxt.clear()
    ptxt.show()

if __name__ == '__main__':
    ptxt = progress.ProgressText('Searching{progress}', '...')
    thread = threading.Thread(target=update_progtxt)
    thread.start()

    while True:
        time.sleep(random.randint(3, 8))

    thread.join()
