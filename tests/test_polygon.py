from typing import Union

import matplotlib.pyplot as plt
import pytest

from mathx.polygon import Line, Point, Polygon


@pytest.fixture
def verbose(request) -> int:
    return request.config.getoption("verbose")


############
# Plotters #
############

PLOT_VERBOSITY = 2


def plot_line_contains(line: Line, point: Point) -> None:
    plt.figure()
    plt.plot(line.x(), line.y(), color="blue", marker="o")
    plt.scatter(point[0], point[1], c="red", marker="x")
    plt.show()


def plot_line_intersection(
    line1: Line,
    line2: Line,
    intersection: Union[None, Point, Line],
    exp: Union[None, Point, Line],
) -> None:
    plt.figure()
    for line in [line1, line2]:
        plt.plot(line.x(), line.y(), linestyle="--", marker="o")

    # plt.scatter(intersection[0], intersection[1])

    plt.show()


def plot_polygon_intersection(
    polygon1: Polygon,
    polygon2: Polygon,
    intersection: Union[None, Line, Polygon],
    exp: Union[None, Line, Polygon],
) -> None:
    colors = ["r", "k", "g", "b"]
    hatches = ["x", "", "/", "\\"]

    plt.figure()
    for polygon in [polygon1, polygon2]:
        plt.fill(
            polygon.x(),
            polygon.y(),
            edgecolor="k",
            facecolor="none",
            hatch=hatches.pop(),
        )
        plt.scatter(polygon.x(), polygon.y(), color="k", marker="o")

    for a in [intersection, exp]:
        if isinstance(a, Polygon):
            plt.fill(
                a.x(),
                a.y(),
                edgecolor=colors.pop(),
                facecolor="none",
                hatch=hatches.pop(),
            )
            plt.scatter(a.x(), a.y(), color="r", marker="x")

    plt.gca().axis("equal")
    plt.show()


#########
# Tests #
#########


@pytest.mark.parametrize(
    "line, exp",
    [
        (Line((0, 0), (1, 1)), Line((0, 0), (1, 1))),
        (Line((0, 0), (1, 1)), Line((1, 1), (0, 0))),
    ],
)
def test_line_eq(line: Line, exp: Line) -> None:
    assert line == exp


@pytest.mark.parametrize(
    "line, point, exp",
    [
        (Line((0, 0), (1, 1)), (0, 0), True),
        (Line((0, 0), (1, 1)), (0.5, 0.5), True),
        (Line((0, 0), (1, 1)), (1, 1), True),
        (Line((0, 0), (1, 1)), (1, 0), False),
        (Line((0, 0), (1, 1)), (0, 1), False),
        (Line((0, 0), (1, 1)), (-1, 0), False),
        (Line((0, 0), (1, 1)), (0, -1), False),
        (Line((0, 0), (3, 3)), (1, 1), True),
        (Line((0, 0), (3, 3)), (2, 2), True),
    ],
)
def test_line_contains(
    line: Line,
    point: Point,
    exp: bool,
    verbose: int,
) -> None:
    contains = line.contains(point)

    # Assert
    try:
        assert contains is exp
    except AssertionError as e:
        verbose += 1
        raise e
    finally:
        if verbose >= PLOT_VERBOSITY:
            plot_line_contains(line, point)


@pytest.mark.parametrize(
    "line1, line2, exp",
    [
        (Line((0, 0), (2, 2)), Line((0, 2), (2, 0)), (1, 1)),
        (Line((0, 0), (1, 1)), Line((1, 2), (2, 1)), None),
        (Line((0, 0), (1, 1)), Line((0, 3), (1, 2)), None),
        (Line((0, 0), (1, 1)), Line((1, 1), (2, 0)), (1, 1)),
        (Line((0, 0), (1, 1)), Line((1, 1), (2, 2)), (1, 1)),
        (Line((0, 0), (1, 1)), Line((0, 1), (1, 2)), None),
        (Line((0, 0), (2, 2)), Line((1, 1), (3, 3)), Line((1, 1), (2, 2))),
        (Line((0, 0), (3, 3)), Line((1, 1), (2, 2)), Line((1, 1), (2, 2))),
        (Line((0, 0), (2, 2)), Line((0, 0), (1, 1)), Line((0, 0), (1, 1))),
        (Line((0, 0), (2, 2)), Line((1, 1), (2, 2)), Line((1, 1), (2, 2))),
        (Line((0, 0), (1, 1)), Line((0, 0), (1, 1)), Line((0, 0), (1, 1))),
    ],
)
def test_line_intersection(
    line1: Line,
    line2: Line,
    exp: Union[None, Point, Line],
    verbose: int,
) -> None:
    intersection = line1.intersection(line2)

    # Assert
    try:
        assert intersection == exp
    except AssertionError as e:
        verbose += 1
        raise e
    finally:
        if verbose >= PLOT_VERBOSITY:
            plot_line_intersection(line1, line2, intersection, exp)


@pytest.mark.parametrize(
    "polygon, exp",
    [
        (
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        ),
        (
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(1, 0), (1, 1), (0, 1), (0, 0)]),
        ),
    ],
)
def test_polygon_eq(polygon: Polygon, exp: Polygon) -> None:
    assert polygon == exp


@pytest.mark.parametrize(
    "polygon, exp",
    [
        (
            Polygon([(0, 0), (0.5, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        ),
        (
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0.5)]),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        ),
        (
            Polygon([(0, 0), (0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        ),
    ],
)
def test_polygon_simplify(polygon: Polygon, exp: Polygon) -> None:
    assert polygon.reduce() == exp


@pytest.mark.parametrize(
    "polygon, exp",
    [
        (Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), True),
        (Polygon([(1, 1), (2, 1), (2, 2), (1, 2), (0.5, 1.5)]), True),
        (Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]), False),
        (Polygon([(0, 0), (0, 0), (1, 0), (1, 1), (0, 1)]), True),
    ],
)
def test_polygon_convex(polygon: Polygon, exp: bool) -> None:
    assert polygon.convex() == exp


@pytest.mark.parametrize(
    "polygon, point, exp",
    [
        (Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]), (1, 1), True),
        (Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]), (1, 2), True),
        (Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), (1, 1), True),
        (Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]), (2, -1), False),
    ],
)
def test_polygon_contains(polygon: Polygon, point: Point, exp: bool) -> None:
    assert polygon.contains(point) == exp


@pytest.mark.parametrize(
    "polygon1, polygon2, exp",
    [
        (
            Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
            Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
            Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
        ),
        (
            Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
            Polygon([(1, 1), (3, 1), (3, 3), (1, 3)]),
            Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
        ),
        (
            Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
            Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
            Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
        ),
        (
            Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]),
            Polygon([(-1, 2), (2, -1), (5, 2), (2, 5)]),
            Polygon([(0, 1), (1, 0), (3, 0), (4, 1), (4, 3), (3, 4), (1, 4), (0, 3)]),
        ),
        (
            Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
            Polygon([(1, 2), (2, 2), (2, 4), (1, 4)]),
            Polygon([(1, 2), (2, 2), (2, 3), (1, 3)]),
        ),
        (
            Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
            Polygon([(1, -1), (2, -1), (2, 2), (1, 2)]),
            Polygon([(1, 0), (2, 0), (2, 2), (1, 2)]),
        ),
        (
            Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
            Polygon([(1, 1), (3, 1), (3, 4), (1, 4)]),
            Polygon([(1, 1), (3, 1), (3, 3), (1, 3)]),
        ),
        (
            Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
            Polygon([(1, 1), (3, 1), (3, 2), (1, 2)]),
            Polygon([(1, 1), (3, 1), (3, 2), (1, 2)]),
        ),
        (
            Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
            Polygon([(3, 1), (5, 1), (5, 4), (3, 4)]),
            Line((3, 1), (3, 3)),
        ),
    ],
)
def test_polygon_intersection(
    polygon1: Polygon,
    polygon2: Polygon,
    exp: Union[None, Line, Polygon],
    verbose: int,
) -> None:
    intersection = polygon1.intersection(polygon2)

    # Assert
    try:
        assert intersection == exp
    except AssertionError as e:
        verbose += 1
        raise e
    finally:
        if verbose >= PLOT_VERBOSITY:
            plot_polygon_intersection(polygon1, polygon2, intersection, exp)
