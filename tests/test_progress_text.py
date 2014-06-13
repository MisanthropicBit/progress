#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for the progress.ProgressText class."""

__date__ = '2014-06-13'  # YYYY-MM-DD

import pytest
import progress


def test_progresstext():
    with pytest.raises(ValueError):
        progress.ProgressText('', '')

    with pytest.raises(ValueError):
        progress.ProgressText(None, '')

    with pytest.raises(ValueError):
        progress.ProgressText('{progress} {progress}', '')

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

    testtext.fmt = 'Searching {progress}'
    assert len(testtext) == 11
    assert str(testtext) == 'Searching |'

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
