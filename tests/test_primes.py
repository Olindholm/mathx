#!/usr/bin/env python3
import pytest

#
# Prime Number Test
#
from mathx import prime_number

def test_prime_number_float_input():
    n = 2.0

    with pytest.raises(TypeError):
        prime_number(n)

def test_prime_number_none_input():
    with pytest.raises(TypeError):
        prime_number(None)

def test_prime_number_negative():
    n = -2

    with pytest.raises(ValueError):
        prime_number(n)

def test_prime_number_zero():
    n = 0

    with pytest.raises(ValueError):
        prime_number(n)

def test_prime_number_one():
    n = 1
    expect = 2
    assert prime_number(n) == expect

def test_prime_number_positive():
    n = 10
    expect = 29
    assert prime_number(n) == expect
