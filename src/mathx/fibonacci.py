#!/usr/bin/env python3

# Recursive
def fibonacci_number_recursive_solver(n):
    if (n < 0):
        return (-1 if (n % 2) == 0 else 1) * fibonacci_number_recursive_solver(-n)

    if (n <= 1):
        return n

    return fibonacci_number_recursive_solver(n-1) + fibonacci_number_recursive_solver(n-2)

fibonacci_number_solvers = {
    "recursive_solver": fibonacci_number_recursive_solver,
}

def fibonacci_number(n, solver="recursive_solver"):
    return fibonacci_number_solvers[solver](n)
