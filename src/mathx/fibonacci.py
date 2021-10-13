#!/usr/bin/env python3
from numbers import Integral

def isinteger(n):
    ""
    return isinstance(n, int)

# Recursive
def _fibonacci_number_recursive_solver(n):
    # Ensure n is a integer
    if (not isinstance(n, int)):
        raise TypeError("n must be an integer!")

    # If n is negative
    if (n < 0):
        return (-1 if (n % 2) == 0 else 1) * _fibonacci_number_recursive_solver(-n)

    if (n <= 1):
        return n

    return _fibonacci_number_recursive_solver(n-1) + _fibonacci_number_recursive_solver(n-2)

# Iterative
def _fibonacci_number_iterative_solver(n):
    if (n < 0):
        return (-1 if (n % 2) == 0 else 1) * _fibonacci_number_iterative_solver(-n)

    if (n <= 1):
        return n

    Fn_sub1 = 1
    Fn_sub2 = 0
    for i in range(2, n):
        Fn = Fn_sub1 + Fn_sub2

        Fn_sub2 = Fn_sub1
        Fn_sub1 = Fn

    return Fn_sub1 + Fn_sub2

fibonacci_number_solvers = {
    "recursive_solver": _fibonacci_number_recursive_solver,
    "iterative_solver": _fibonacci_number_iterative_solver,
}

# Calculates and returns the nth fibonacci number.
# n must be an integer (whole number).
#
def fibonacci_number(n, solver="recursive_solver"):
    return fibonacci_number_solvers[solver](n)
