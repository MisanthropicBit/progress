#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for the progress.ProgressText class."""

__date__ = '2014-05-22'  # YYYY-MM-DD

import pytest
import progress


def test_progresstext_init():
    with pytest.raises(ValueError):
        progress.ProgressText('', '')

    with pytest.raises(ValueError):
        progress.ProgressText(None, '')

    with pytest.raises(ValueError):
        progress.ProgressText('{progress} {progress}', '')
