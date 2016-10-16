#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for testing ETA classes."""

import progress.eta
import pytest

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
    ema = progress.eta.EMAETA()
    expected = [323.33333333333326, 159.5744680851063606, 98.2800982800982723,
                55.458436313219600, 24.5715338780023309]

    assert ema.get() is None
    run_eta_test(times, values, expected, ema, maxvalue)

    assert ema.format_eta(1000) == [0, 16, 40]
    assert ema.format_eta(9512) == [2, 38, 32]
    assert ema.format_eta(2) == [0, 0, 2]
    assert ema.format_eta(-60) == [-1, 59, 0]

    with pytest.raises(ValueError):
        ema.decay = -1.0

    with pytest.raises(ValueError):
        ema.decay = 1.2

    assert ema.get() == [0, 0, 24]


def test_sma_eta():
    sma = progress.eta.SMAETA(3)
    expected = [32.333333333333336, 30., 26.181818181818183,
                20.674157303370787, 8.994082840236686]

    assert sma.get() is None
    run_eta_test(times, values, expected, sma, maxvalue)
    assert sma.get() == [0, 0, 8]


def test_sma_eta_fail():
    sma = progress.eta.SMAETA(3)

    with pytest.raises(ValueError):
        sma.window = 0


def test_wrong_eta_return_type():
    class FailETA1(progress.eta.BaseETA):
        def update(self, time, value, maxval):
            pass

        def get(self):
            return ""

    class FailETA2(progress.eta.BaseETA):
        def update(self, time, value, maxval):
            pass

        def get(self):
            return range(4)

    with pytest.raises(ValueError):
        testbar = progress.ProgressBar("{hours}", etaobj=FailETA1())
        testbar.update(10)

    with pytest.raises(ValueError):
        testbar = progress.ProgressBar("{hours}", etaobj=FailETA2())
        testbar.update(10)
