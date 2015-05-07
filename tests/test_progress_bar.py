#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for the progress.ProgressBar class."""

# TODO: Test width/char/head with strings of len() > 1

import sys
import pytest
import progress
import progress.eta

__date__ = '2015-05-05'  # YYYY-MM-DD


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


def approx_equals(a, b):
    """Return True if the difference between a and b is very small."""
    return (a - b) < 1.5e-16


def test_progressbar():
    # Test keyword arguments that should fail
    for kwargs in fail_kwargs:
        with pytest.raises(ValueError):
            progress.ProgressBar(**kwargs)

    testbar = progress.ProgressBar('[{progress}]')
    assert testbar.min == 0
    assert testbar.max == 100
    assert testbar.char == '='
    assert testbar.head == '>'
    assert testbar.width == 20
    assert len(testbar) == len('[' + (testbar.fill * testbar.width) + ']')
    assert not testbar._has_eta
    assert testbar._etaobj is None

    with pytest.raises(ValueError):
        testbar.char = ''

    with pytest.raises(ValueError):
        testbar.head = ''

    with pytest.raises(ValueError):
        testbar.fill = ''

    with pytest.raises(ValueError):
        testbar.char = '**'

    with pytest.raises(ValueError):
        testbar.head = ')))'

    with pytest.raises(ValueError):
        testbar.fill = 'urso'

    with pytest.raises(ValueError):
        testbar.width = 0

    with pytest.raises(ValueError):
        testbar.width = -20

    with pytest.raises(ValueError):
        testbar.min = 100

    with pytest.raises(ValueError):
        testbar.min = 101

    with pytest.raises(ValueError):
        testbar.max = 0

    with pytest.raises(ValueError):
        testbar.max = -1

    # Attempt to update with a negative value
    with pytest.raises(ValueError):
        testbar.update(-10)

    with pytest.raises(ValueError):
        testbar += -20

    # Test failing ETA objects
    for etaobj in (FailETA1(), FailETA2(), FailETA3()):
        with pytest.raises(ValueError):
            progress.ProgressBar(fmt=' ', etaobj=etaobj)

    # Test updates/states through properties
    testbar.value = 50
    assert testbar.value == 50
    assert testbar.percent == 0.5
    assert testbar.max == 100
    assert testbar.target is sys.stderr

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

    # Test proper reset
    testbar.reset()
    assert testbar.value == 0
    assert testbar.percent == 0.0
    assert str(testbar) == '[' + testbar.head +\
        (testbar.fill * (testbar.width - 1)) + ']'
    assert not testbar.done()

    # Test autoupdate feature
    testbar.autoupdate(22)
    assert testbar.value == 22
    assert testbar.percent == 0.22
    assert testbar.min == 0
    assert not testbar.done()

    # Test 'percent' property
    testbar.percent = 0.73408248
    assert approx_equals(testbar.percent, 0.73408248)
    assert testbar.value == testbar.max * 0.73408248
    assert testbar.min == 0
    assert testbar.max == 100

    # Test 'width' property
    testbar.width = 30
    assert testbar.width == 30
    assert str(testbar) == '[' +\
        (testbar.char * (int(testbar.width * 0.75) - 1)) + testbar.head +\
        (testbar.fill * (int(testbar.width * 0.25) + 1)) + ']'

    # Test visual feature updates through properties
    testbar.value = 0
    testbar += 50
    testbar.max = 200
    assert testbar.max == 200
    assert testbar.min == 0
    testbar.head = '?'
    assert testbar.head == '?'
    testbar.char = '@'
    assert testbar.char == '@'
    testbar.fill = '_'
    assert testbar.fill == '_'
    assert str(testbar) == '[' +\
        ('@' * (int(testbar.width * 0.25) - 1)) + '?' +\
        ('_' * (int(testbar.width * 0.75) + 1)) + ']'
    assert testbar.target is sys.stderr

    # Test setting the 'min' property
    testbar.min = -10
    assert testbar.min == -10
    assert testbar.max == 200
    assert testbar.value == 50
    assert approx_equals(testbar.percent, 0.2857142857142857)

    testbar.value = 95
    assert testbar.value == 95
    assert approx_equals(testbar.percent, 0.5)

    assert type(testbar.format) is str
    testbar.format = "{percentage}%"
    assert testbar.format == "{percentage}%"

    # Test setting an ETA
    testbar.format = "{progress} {percentage}% {minutes}"
    assert testbar._has_eta

    # Fails due to 'progress' key being used twice
    with pytest.raises(ValueError):
        testbar.format = "{progress} {progress}"

    # Fails due to an empty format string
    with pytest.raises(ValueError):
        testbar.format = ""

    # Test switching targets
    testbar.target = sys.stdout
    assert testbar.target is sys.stdout

    with pytest.raises(ValueError):
        testbar.target = sys.stdin

    l = list(range(3))
    d = dict(a=1, b=3)
    testbar.show(*l, **d)
    testbar.autoupdate(10, *l, **d)

    # Fails because progress is a reserved key
    with pytest.raises(ValueError):
        d['progress'] = 'I am not allowed :('
        testbar.autoupdate(5, **d)
