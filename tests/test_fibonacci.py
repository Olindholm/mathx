#!/usr/bin/env python3
import pytest

def fibonacci_number_solver_float_input(fib):
    n = 2.0

    with pytest.raises(TypeError):
        fib(n)

# Generate test functions for every solver
def create_test_cases_for_items(prefix, items, scope=globals()):

    # Find all tests
    tests = [(name[len(prefix):], thing) for (name, thing) in scope.items() if callable(thing) and name.startswith(prefix)]

    for (item_name, item_func) in items:
        for (test_name, test_func) in tests:
            name = "test_" + prefix + item_name + "_" + test_name
            func = lambda test=test_func, func=item_func: test(func)
            scope[name] = func

from mathx import fibonacci_number_solvers
create_test_cases_for_items("fibonacci_number_", fibonacci_number_solvers.items())
