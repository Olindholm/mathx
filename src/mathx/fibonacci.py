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
    # Ensure n is a integer
    if (not isinstance(n, int)):
        raise TypeError("n must be an integer!")

    # If n is negative
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

from math import log2, ceil

# Knuth Fibonacci
# http://www.davidespataro.it/yet-another-one-on-fibonacci-serie-knuth-multiplication/
# TODO REVIEW THIS?
# https://muthu.co/fast-nth-fibonacci-number-algorithm/

def _fibonacci_number_knuth_solver(n):
    # Ensure n is a integer
    if (not isinstance(n, int)):
        raise TypeError("n must be an integer!")

    # If n is negative
    if (n < 0):
        return (-1 if (n % 2) == 0 else 1) * _fibonacci_number_knuth_solver(-n)

    if (n <= 1):
        return n

    # Donald E. Knuth Method
    # Fn = Q^(n-1) [0, 0]
    n = n-1
    matrices = []
    Q = [ [1, 1], [1, 0] ]

    m = 1
    if (n & m): matrices.append(Q)
    for i in range(1, ceil(log2(n))):
        #
        Q = matrix_multiplication(Q, Q)
        m = m << 1

        if (n & m): matrices.append(Q)

    M = matrices[0]
    for i in range(1, len(matrices)):
        M = matrix_multiplication(M, matrices[i])

    return M[0][0]

def matrix_multiplication(A, B):
    n = len(A)
    m = len(A[0])
    r = len(B[0])

    C = []
    for i in range(n):
        row = []

        for j in range(r):
            c = 0

            for k in range(m):
                c = c + A[i][k] * B[k][j]

            row.append(c)

        C.append(row)

    return C

fibonacci_number_solvers = {
    "recursive_solver": _fibonacci_number_recursive_solver,
    "iterative_solver": _fibonacci_number_iterative_solver,
    "knuth_solver": _fibonacci_number_knuth_solver,
}

# Calculates and returns the nth fibonacci number.
# n must be an integer (whole number).
#
def fibonacci_number(n, solver="knuth_solver"):
    if (solver not in fibonacci_number_solvers):
        raise ValueError("Unsuported solver!")

    return fibonacci_number_solvers[solver](n)
