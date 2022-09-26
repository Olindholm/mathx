from __future__ import annotations

from typing import List, Tuple, Union

import numpy as np
from numpy.linalg import norm

Point = Tuple[float, float]
PointList = List[Point]


def dist(p1: Point, p2: Point) -> float:
    a = np.array(p1)
    b = np.array(p2)
    return norm(b - a)


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def x(self) -> List[float]:
        return [self.p1[0], self.p2[0]]

    def y(self) -> List[float]:
        return [self.p1[1], self.p2[1]]

    def contains(self, p: Point) -> bool:
        # If C is on the AB line. Then the following must hold
        # |AC| + |CB| == |AB|
        a = np.array(self.p1)
        b = np.array(self.p2)
        c = np.array(p)
        return bool(np.isclose(norm(c - a) + norm(b - c), norm(b - a)))

    def intersection(self, line: Line) -> Union[None, Point, Line]:
        # Find intersection point
        s = np.vstack([self.p1, self.p2, line.p1, line.p2])
        h = np.hstack((s, np.ones((4, 1))))
        l1 = np.cross(h[0], h[1])
        l2 = np.cross(h[2], h[3])
        x, y, z = np.cross(l1, l2)
        if z != 0:
            i = (x / z, y / z)
            return i if self.contains(i) and line.contains(i) else None

        # Find intersection line
        # TODO this might need to be an ordered set?
        c = set()
        for line1, line2 in [(self, line), (line, self)]:
            if line1.contains(line2.p1):
                c.add(line2.p1)
            if line1.contains(line2.p2):
                c.add(line2.p2)

        if len(c) == 1:
            return c.pop()
        elif len(c) == 2:
            return Line(c.pop(), c.pop())

        return None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.p1}, {self.p2})"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Line):
            return {self.p1, self.p2} == {o.p1, o.p2}

        return NotImplemented


class Polygon:
    def __init__(self, points: PointList) -> None:
        self.points = points

    def __repr__(self) -> str:
        return f"Polygon({self.points})"

    def x(self) -> List[float]:
        return [p[0] for p in self.points]

    def y(self) -> List[float]:
        return [p[1] for p in self.points]

    def pairs(self) -> List[Tuple[Point, Point]]:
        n = len(self.points)
        return [(self.points[i], self.points[(i + 1) % n]) for i in range(n)]

    def reduce(self) -> Polygon:
        points = [*self.points]

        i = 1
        while i < len(points):
            a = points[i - 1]
            m = points[i]
            b = points[i + 1 - len(points)]

            if Line(a, b).contains(m):
                points.pop(i)
            else:
                i += 1

        return Polygon(points)

    def convex(self) -> bool:
        points = np.array(self.points)
        deltas = np.roll(points.copy(), -1, axis=0) - points
        phases = np.arctan2(deltas[:, 1], deltas[:, 0]) % (2 * np.pi)
        angles = phases[1:] - phases[:-1]
        return (angles >= 0).all()

    def contains(self, p: Point) -> bool:
        # Is it inside?
        point = np.array(p)

        points = np.array(self.points)
        deltas = np.roll(points.copy(), -1, axis=0) - points
        phases = np.arctan2(deltas[:, 1], deltas[:, 0]) % (2 * np.pi)

        d = point - points
        ph = np.arctan2(d[:, 1], d[:, 0]) % (2 * np.pi)

        if (ph >= phases).all():
            return True

        # Is it on the borders?
        for p1, p2 in self.pairs():
            if Line(p1, p2).contains(p):
                return True

        # Guess not
        return False

    def intersection(self, polygon: Polygon) -> Union[None, Point, Line, Polygon]:
        if self.convex() is False:
            raise NotImplementedError()

        points = []
        for a, b in polygon.pairs():
            ab = Line(a, b)

            if self.contains(a):
                points.append(a)

            intersections = []
            for c, d in self.pairs():
                cd = Line(c, d)

                i = ab.intersection(cd)
                if isinstance(i, Point.__origin__):
                    intersections.append(i)
                elif isinstance(i, Line):
                    intersections.append(i.p1)
                    intersections.append(i.p2)

            intersections.sort(key=lambda x: dist(a, x))
            points.extend(intersections)

        # Reduce to unique points
        points = dict.fromkeys(points)
        n = len(points)

        if n == 0:
            return None
        elif n == 1:
            return points[0]
        elif n == 2:
            return Line(*points)
        else:
            return Polygon(points).reduce()

    def __eq__(self, o: object) -> bool:
        # TODO
        # Should I reduce before comparing?
        if isinstance(o, Polygon):
            p0 = self.points[0]
            if p0 not in o.points:
                return False

            i = o.points.index(p0)
            return self.points == o.points[i:] + o.points[:i]

        return NotImplemented
