#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for testing ETA classes."""

import progress.eta

__date__ = '2015-04-14'  # YYYY-MM-DD


def approx_equals(a, b):
    """Return True if the difference between a and b is very small."""
    return abs(a - b) < 1.5e-16


def run_eta_test(times, values, expected, eta, maxvalue):
    """Run a test on the output of an ETA object."""
    # Compare the expected value with the calculation from an ETA object
    for t, v, e in zip(times, values, expected):
        eta.update(t, v, maxvalue)

        if eta.eta is not None:
            assert approx_equals(e, eta.eta)


def test_simple_eta():
    """Test the progress.eta.SimpleETA class."""
    maxvalue = 100.
    times = [1., 12., 20., 25., 26.]
    values = [3., 25, 40, 54, 62]
    expected = [32.333333333333336, 37.5, 32.0, 16.42857142857143, 4.75]

    eta = progress.eta.SimpleETA()

    # Run test with predefined values
    run_eta_test(times, values, expected, eta, maxvalue)


def test_ema_eta():
    """Test the progress.eta.EMAETA class."""
    times = [1., 12., 20., 25., 26.]
    values = [3., 25, 40, 54, 62]
    expected = [323.33333333333326, 159.5744680851063606, 98.2800982800982723,
                55.458436313219600, 24.5715338780023309]

    eta = progress.eta.EMAETA()

    run_eta_test(times, values, expected, eta, 100.)
