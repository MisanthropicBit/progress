#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for the progress.ProgressText class."""

__date__ = '2015-02-03'  # YYYY-MM-DD

import sys
import pytest
import progress


def test_progresstext():
    # Test initialisation errors
    with pytest.raises(ValueError):
        progress.ProgressText('', '')

    with pytest.raises(ValueError):
        progress.ProgressText(None, '')

    with pytest.raises(ValueError):
        progress.ProgressText('{progress} {progress}', '')

    # Test basic properties
    testtext = progress.ProgressText('Searching{progress}', '...')
    assert testtext.value == '.'

    testtext.update()
    assert testtext.value == '..'

    testtext.update()
    assert testtext.value == '...'

    testtext.autoupdate()
    assert testtext.value == '.'

    testtext.progress = '|/-\\'
    testtext.autoreset = True
    assert testtext.value == '|'
    assert testtext.autoreset is True

    testtext.format = 'Searching {progress}'
    assert testtext.value == '|'
    assert len(testtext) == 11
    assert str(testtext) == 'Searching |'

    testtext.target = sys.stdout
    assert testtext.target is sys.stdout

    testtext.target = sys.stderr
    assert testtext.target is sys.stderr

    # Should fail because only sys.stdout and sys.stderr are allowed
    with pytest.raises(ValueError):
        testtext.target = sys.stdin

    with pytest.raises(ValueError):
        testtext.target = "sys.fail"

    testtext.update()
    assert testtext.value == '/'

    testtext.autoupdate()
    assert testtext.value == '-'

    testtext.update()
    assert testtext.value == '\\'
    assert str(testtext) == 'Searching \\'
    assert len(testtext) == 11

    l = list(range(3))
    d = dict(a=1, b=3)
    testtext.show(*l, **d)
    testtext.autoupdate(*l, **d)

    # Should fail because you cannot use reserved keys
    with pytest.raises(ValueError):
        d['progress'] = 'I am not allowed :('
        testtext.autoupdate(**d)

    testtext = progress.ProgressText('Searching{progress}', '...',
                                     include_empty=True)

    assert testtext.value == ''

    testtext.update()
    assert testtext.value == '.'

    testtext.update()
    assert testtext.value == '..'

    testtext.update()
    assert testtext.value == '...'

    testtext.update()
    assert testtext.value == ''
