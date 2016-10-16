#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test function decorators."""

import progress
import progress.decorators
import pytest
import types
import sys


class Base(object):
    def method():
        """This is a docstring."""
        pass


@progress.decorators.inherit_docstrings
class Derived(Base):
    def method():
        pass


def test_docstring_decorator():
    b = Base()
    d = Derived()

    assert b.method.__doc__ == "This is a docstring."
    assert d.method.__doc__ == "This is a docstring."


def test_docstring_fail():
    with pytest.raises(RuntimeError):
        @progress.decorators.inherit_docstrings
        def fail_method():
            pass


@pytest.mark.skipif(sys.version_info[0] > 2, reason="requires python2")
def test_class_type2():
    assert isinstance(progress.decorators.ClassType('name',
                                                    tuple(),
                                                    dict()), types.ClassType)


@pytest.mark.skipif(sys.version_info[0] < 3, reason="requires python3")
def test_class_type3():
    assert isinstance(progress.decorators.ClassType('name',
                                                    tuple(),
                                                    dict()), type)
