#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for testing ETA classes."""

import pytest
import progress.eta

__date__ = '2015-03-04'  # YYYY-MM-DD


def approx_equals(a, b):
    """Return True if the difference between a and b is very small."""
    return (a - b) < 1.5e-16


def test_simple_eta():
    """Test the progress.eta.SimpleETA class."""
    times = [12., 20., 25., 26.]
    expected_values = []

    eta = progress.eta.SimpleETA()


def test_ema_eta():
    """Test the progress.eta.EMAETA class."""
    times = [12., 20., 25., 26.]
    expected_values = []

    eta = progress.eta.EMAETA()
