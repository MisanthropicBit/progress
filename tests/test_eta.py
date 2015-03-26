#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for testing ETA classes."""

import pytest
import random
import progress.eta

__date__ = '2015-03-26'  # YYYY-MM-DD


try:
    irange = xrange
except NameError:
    irange = range


def generate_updates(mintime, maxtime, minvalue, maxvalue,
                     deltatime, deltavalue):
    """Return a generator that generates incremental time-value pairs."""
    t, v = mintime, minvalue

    while t < mintime or v < maxvalue:
        t += random.uniform(0., deltatime)
        v += random.uniform(0., deltavalue)
        t = min(t, maxtime)
        v = min(v, maxvalue)
        yield t, v

    if v < maxvalue:
        # Yield final value of 100%
        yield t, maxvalue


def approx_equals(a, b):
    """Return True if the difference between a and b is very small."""
    return abs(a - b) < 1.5e-16


def run_eta_test(times, values, eta):
    """Run a test on the output of an ETA object."""
    prev_time, prev_value, manual_eta = 0., 0., 0.

    # Compare the expected value with the calculation from an ETA object
    for t, v in zip(times, values):
        eta.update(t, v, 100.)

        dv, dt = abs(v - prev_value), abs(t - prev_time)

        if dt > 0. and dv > 0.:
            manual_eta = float(100. - v) / (dv / dt)

        if eta.eta is not None:
            assert approx_equals(manual_eta, eta.eta)

        # Set previous values
        prev_time, prev_value = t, v


def test_simple_eta():
    """Test the progress.eta.SimpleETA class."""
    times = [1., 12., 20., 25., 26.]
    values = [0., 25, 40, 54, 62]

    eta = progress.eta.SimpleETA()

    # Run test with predefined values
    run_eta_test(times, values, eta)

    # Do the same, but with randomly generated values
    eta.reset()
    times, values = zip(*list(generate_updates(0., 1000., 0, 100, 10., 10.)))
    run_eta_test(times, values, eta)


def test_ema_eta():
    """Test the progress.eta.EMAETA class."""
    times = [1., 12., 20., 25., 26.]
    values = [0., 25, 40, 54, 62]

    eta = progress.eta.EMAETA()

    run_eta_test(times, values, eta)

    eta.reset()
    times, values = zip(*list(generate_updates(0., 1000., 0, 100, 10., 10.)))
    run_eta_test(times, values, eta)
