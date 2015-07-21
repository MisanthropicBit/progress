#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for the progress.ProgressText class."""


import sys
import pytest
import progress

__date__ = '2015-07-19'  # YYYY-MM-DD


def test_value_property():
    testtext = progress.ProgressText('Searching{progress}', '...')

    assert testtext.value == '.'
    assert not testtext.autoreset

    testtext.update()
    assert testtext.value == '..'
    assert not testtext.include_empty

    testtext.update()
    assert testtext.value == '...'

    testtext.autoupdate()
    assert testtext.value == '.'


def test_initialisation_errors():
    with pytest.raises(ValueError):
        progress.ProgressText('', '')

    with pytest.raises(ValueError):
        progress.ProgressText(None, '')

    with pytest.raises(ValueError):
        progress.ProgressText('{progress} {progress}', '')


def test_output_targets():
    testtext = progress.ProgressText('Searching{progress}', '...')

    assert testtext.target is sys.stderr

    testtext.target = sys.stdout
    assert testtext.target is sys.stdout

    testtext.target = sys.stderr
    assert testtext.target is sys.stderr

    # Should fail because only sys.stdout and sys.stderr are allowed
    with pytest.raises(ValueError):
        testtext.target = sys.stdin

    with pytest.raises(ValueError):
        testtext.target = "sys.fail"

    # Test switching targets
    testtext.target = sys.stdout
    assert testtext.target is sys.stdout

    with pytest.raises(ValueError):
        testtext.target = sys.stdin


def test_updates():
    testtext = progress.ProgressText('Searching {progress}', '|/-\\',
                                     autoreset=True)

    testtext.update()
    assert testtext.value == '/'

    testtext.autoupdate()
    assert testtext.value == '-'

    testtext.update()
    assert testtext.value == '\\'
    assert str(testtext) == 'Searching \\'
    assert len(testtext) == 11

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

    # Test the include_empty property
    testtext.include_empty = True
    assert testtext.value == ''

    testtext.update()
    assert testtext.value == '.'

    testtext.update()
    assert testtext.value == '..'

    testtext.update()
    assert testtext.value == '...'
    assert testtext.include_empty

    testtext.update()
    assert testtext.value == ''


def test_autoreset():
    testtext = progress.ProgressText('Searching{progress}', '...')

    testtext.progress = '|/-\\'
    assert testtext.progress == '|/-\\'
    testtext.autoreset = True
    assert testtext.value == '|'
    assert testtext.autoreset is True


def test_format():
    testtext = progress.ProgressText('Searching{progress}', '|/-\\')

    testtext.format = 'Searching {progress}'
    assert testtext.format == 'Searching {progress}'
    assert testtext.value == '|'
    assert len(testtext) == 11
    assert str(testtext) == 'Searching |'


def test_keyword_arguments():
    testtext = progress.ProgressText('Searching{progress}', '...')

    l = list(range(3))
    d = dict(a=1, b=3)
    testtext.show(*l, **d)
    testtext.autoupdate(*l, **d)
    assert testtext.target is sys.stderr


def test_reserved_keys():
    testtext = progress.ProgressText('Searching{progress}', '...')
    d = dict()

    # Should fail because you cannot use reserved keys
    with pytest.raises(ValueError):
        d['progress'] = 'I am not allowed :('
        testtext.autoupdate(**d)
