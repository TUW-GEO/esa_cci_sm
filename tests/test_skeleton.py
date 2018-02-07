#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from hsaf_cci_042.skeleton import fib

__author__ = "Manuel Schmitzer"
__copyright__ = "Manuel Schmitzer"
__license__ = "none"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
