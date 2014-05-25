#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for the progress.ProgressBar class."""

__date__ = '2014-05-22'  # YYYY-MM-DD

import pytest
import progress
import progress.eta


fail_kwargs = [
    # Should fail because of missing format
    dict(fmt=''),
    # Should fail because width is zero
    dict(fmt=' ', width=0),
    # Fails because of negative width
    dict(fmt=' ', width=-1),
    # Should fail because len(char) is > 1
    dict(fmt=' ', char='!='),
    # Should fail because 'char' arg is too long
    dict(fmt=' ', char='x' * 21),
    # Should fail because 'head' arg is too long
    dict(fmt=' ', head='x' * 21),
    # Should fail because 'char'+'head' args are too long
    dict(fmt=' ', char='x' * 10, head='x' * 11),
    # Should fail because '{progress}' appears twice
    dict(fmt='{progress} {progress}'),
    # Should fail because 'etaobj' does not derive from
    # progress.eta.BaseETA
    dict(fmt=' ', etaobj=type('SomeType', (), dict())),
]


class FailETA1(progress.eta.BaseETA):

    """Fails because get returns more than three elements."""

    def __init__(self):
        pass

    def get(self):
        return (1, 2, 3, 4)


class FailETA2(progress.eta.BaseETA):

    """Fails because get returns an unexpected type."""

    def __init__(self):
        pass

    def get(self):
        return str()


class FailETA3(object):

    """Fails because it does not derive from progress.eta.BaseETA."""

    pass


def test_progressbar():
    # Test keyword arguments that should fail
    for kwargs in fail_kwargs:
        with pytest.raises(ValueError):
            progress.ProgressBar(**kwargs)

    testbar = progress.ProgressBar(' ')
    assert testbar.min == 0
    assert testbar.max == 100
    assert testbar.char == '='
    assert testbar.head == '>'
    assert testbar.width == 20

    # Attempt to update with a negative value
    with pytest.raises(ValueError):
        testbar.update(-10)

    with pytest.raises(ValueError):
        testbar += -20

    # Test failing ETA objects
    for etaobj in (FailETA1(), FailETA2(), FailETA3()):
        with pytest.raises(ValueError):
            progress.ProgressBar(fmt=' ', etaobj=etaobj)

    # Test updates and states
    testbar.value = 50
    assert testbar.value == 50
    assert testbar.percent == 0.5

    testbar.update(25)
    assert testbar.value == 75
    assert testbar.percent == 0.75

    testbar.value = 10
    assert testbar.value == 10
    assert testbar.percent == 0.10

    testbar += 50
    assert testbar.value == 60
    assert testbar.percent == 0.60

    testbar.value = -10
    assert testbar.value == 0
    assert testbar.percent == 0.0

    testbar.value = 1000
    assert testbar.value == 100
    assert testbar.percent == 1.0
    assert testbar.done()

    testbar.reset()
    assert testbar.value == 0
    assert testbar.percent == 0.0
    assert not testbar.done()
