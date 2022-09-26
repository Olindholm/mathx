from typing import Any, Callable, Dict

import pytest

#
# Fibonacci Number Test
#
from mathx import fibonacci_number, fibonacci_number_solvers


def test_fibonacci_number_invalid_solver() -> None:
    n = 10
    solver = "INAVLID_SOVLER"

    # Ensure the invalid solver actually isn't a solver
    assert solver not in fibonacci_number_solvers

    # Test what happens when it is used.
    with pytest.raises(ValueError):
        fibonacci_number(n, solver)  # type: ignore


#
# Fibonacci Solver Tests
#


def fibonacci_number_solver_float_input(fib: Callable[[int], int]) -> None:
    n = 2.0

    with pytest.raises(TypeError):
        fib(n)  # type: ignore


def fibonacci_number_solver_none_input(fib: Callable[[int], int]) -> None:
    with pytest.raises(TypeError):
        fib(None)  # type: ignore


def fibonacci_number_solver_zero(fib: Callable[[int], int]) -> None:
    n = 0
    expect = 0
    assert fib(n) == expect


def fibonacci_number_solver_one(fib: Callable[[int], int]) -> None:
    n = 1
    expect = 1
    assert fib(n) == expect


def fibonacci_number_solver_two(fib: Callable[[int], int]) -> None:
    n = 2
    expect = 1
    assert fib(n) == expect


def fibonacci_number_solver_positive(fib: Callable[[int], int]) -> None:
    n = 10
    expect = 55
    assert fib(n) == expect


def fibonacci_number_solver_negative(fib: Callable[[int], int]) -> None:
    n = -10
    expect = -55
    assert fib(n) == expect


# Generate test functions for every solver
def create_test_cases_for_items(
    prefix: str,
    items: Dict[str, Callable],
    scope: Dict[str, Any] = globals(),
) -> None:

    # Find all tests
    tests = [
        (name[len(prefix) :], thing)
        for name, thing in scope.items()
        if callable(thing) and name.startswith(prefix)
    ]

    for item_name, item_func in items.items():
        for (test_name, test_func) in tests:
            name = "test_" + prefix + item_name + "_" + test_name
            func = lambda test=test_func, func=item_func: test(func)
            scope[name] = func


create_test_cases_for_items("fibonacci_number_", fibonacci_number_solvers)
