#!/usr/bin/env python3
import pytest

def fibonacci_number_solver_float_input(fib):
    n = 2.0

    with pytest.raises(TypeError):
        fib(n)

# Generate test functions for every solver
def hello(prefix, items, scope=globals()):
    print(scope)

    # Find all tests
    tests = [(name[len(prefix):], thing) for (name, thing) in scope.items() if callable(thing) and name.startswith(prefix)]

    for (item_name, item_func) in items:
        for (test_name, test_func) in tests:
            func = lambda: test_func(item_func)
            scope["test_fibonacci_number_" + item_name + "_" + test_name] = func

from mathx import fibonacci_number_solvers
hello("fibonacci_number_solver_", fibonacci_number_solvers.items())
