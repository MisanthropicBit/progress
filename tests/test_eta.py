#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for testing ETA classes."""

import progress.eta
import pytest

__date__ = '2015-07-24'  # YYYY-MM-DD

# Shared time, values and maximum value for testing all ETA classes
times = [1, 12, 20, 25, 26]
values = [3, 25, 40, 54, 62]
maxvalue = 100


def approx_equals(a, b):
    """Return True if the difference between a and b is very small."""
    return abs(a - b) < 1.e-14


def run_eta_test(times, values, expected, eta, maxvalue):
    """Run a test on the output of an ETA object."""
    # Compare the expected value with the calculation from an ETA object
    for t, v, e in zip(times, values, expected):
        eta.update(t, v, maxvalue)

        if eta.eta is not None:
            assert approx_equals(e, eta.eta)


def test_base_eta():
    base_eta = progress.eta.BaseETA()

    with pytest.raises(NotImplementedError):
        base_eta.update(0, 0, 0)

    with pytest.raises(NotImplementedError):
        base_eta.get()

    with pytest.raises(NotImplementedError):
        base_eta.reset()

    with pytest.raises(NotImplementedError):
        base_eta.eta

    assert base_eta.format_eta(1000) == [0, 16, 40]
    assert base_eta.format_eta(9512) == [2, 38, 32]
    assert base_eta.format_eta(2) == [0, 0, 2]
    assert base_eta.format_eta(-60) == [-1, 59, 0]


def test_simple_eta():
    expected = [32.333333333333336, 37.5, 32.0, 16.42857142857143, 4.75]
    run_eta_test(times, values, expected, progress.eta.SimpleETA(), maxvalue)


def test_ema_eta():
    emaeta = progress.eta.EMAETA()
    expected = [323.33333333333326, 159.5744680851063606, 98.2800982800982723,
                55.458436313219600, 24.5715338780023309]
    run_eta_test(times, values, expected, emaeta, maxvalue)

    assert emaeta.format_eta(1000) == [0, 16, 40]
    assert emaeta.format_eta(9512) == [2, 38, 32]
    assert emaeta.format_eta(2) == [0, 0, 2]
    assert emaeta.format_eta(-60) == [-1, 59, 0]

    with pytest.raises(ValueError):
        emaeta.decay = -1.0

    with pytest.raises(ValueError):
        emaeta.decay = 1.2


def test_sma_eta():
    expected = [32.333333333333336, 30., 26.181818181818183,
                20.674157303370787, 8.994082840236686]
    run_eta_test(times, values, expected, progress.eta.SMAETA(3), maxvalue)
