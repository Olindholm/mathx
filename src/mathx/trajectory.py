from math import sqrt

import numpy as np
from matplotlib import pyplot
from numpy import diff
from numpy import sign as sgn


def psgn(x):
    return 1 if x == 0 else sgn(x)


def cumsum(x, prepend=[]):
    return np.concatenate(([0], x)).cumsum()


class Trajectory(object):
    def __init__(self, dt, dv, x0=0, v0=0):
        self._dt = dt
        self._dv = dv

        self._x0 = x0
        self._v0 = v0

    @classmethod
    def fromspeeds(cls, t, v):
        return cls(diff(t), diff(v), v0=v[0])

    def _t(self):
        return cumsum(self._dt, prepend=0)

    def maxtime(self):
        return sum(self._dt)

    def __durations(self, t):
        N = len(self._T) - 1

        for i in range(N):
            T = self._T[i]
            DT = self._T[i + 1] - T
            dt = np.minimum(np.maximum(t - T, 0), DT)

            yield (i, dt)

    def acc(self, t):

        return t

    def vel(self, t):
        ddX = self._ddX

        v = self._dX0 * np.ones(t.shape)
        for i, dt in self.__durations(t):
            v += ddX[i] * dt

        return v

    def pos(self, t):
        ddX = self._ddX
        dX = self.vel(self._T)

        x = self._X0 * np.ones(t.shape)
        for i, dt in self.__durations(t):
            x += dX[i] * dt + ddX[i] / 2 * dt**2

        return x

    def plot(self, Ts=0.1):
        maxtime = self.maxtime()

        # Get
        t = self._t()

        fig, (posax, velax, accax) = pyplot.subplots(3)

        # Acceleration
        accax.step(t, self.acc(t), where="post")
        accax.set_xlim(0, maxtime)

        # Velocity
        # velax.plot(self._T, self.vel(self._T))
        # velax.set_xlim(0, maxtime)

        # Position
        # t = np.linspace(0, maxtime, 1+maxtime/Ts)
        # posax.plot(t, self.pos(t))
        # posax.set_xlim(0, maxtime)

        pyplot.show()


def trajectory(x0, x4, v, dv, v0=0, v4=0):
    # If start and end is same
    # Then there is nothing to plan
    if x0 == x4 and v0 == v4:
        raise NotImplementedError("todo")

    d = x4 - x0
    v = psgn(d) * v

    # Phase 1 (typical acceleration)
    dv1 = psgn(v - v0) * dv
    t1 = (v - v0) / dv1
    d1 = v0 * t1 + dv1 / 2 * t1**2

    # Phase 3 (typical decceleration)
    dv3 = psgn(v4 - v) * dv
    t3 = (v4 - v) / dv3
    d3 = v * t3 + dv3 / 2 * t3**2

    # Phase 2 (typical constant speed)
    t2 = (d - (d1 + d3)) / v

    # If phase 1 and 3 is (larger than total distance)
    # => Phase 2 don't exist and other phases are too long
    if t2 < 0:
        a = 1 / 2 * (dv1 - dv3)
        b = -(v0 + dv1 * t1 + v4 - dv3 * t3)
        c = (v0 * t1 + dv1 / 2 * t1**2 + v4 * t3 - dv3 / 2 * t3**2) - d

        dt = (-b - sqrt(b**2 - 4 * a * c)) / (2 * a)

        # Adjust times
        t1 = t1 - dt
        t2 = 0
        t3 -= dt

        # Adjust speed (v) to maximum reached speed
        v = v0 + dv1 * t1

    T = []
    T.append(0)
    T.append(t1)
    if t2 > 0:
        T.append(t1 + t2)
    T.append(t1 + t2 + t3)

    dX = []
    dX.append(v0)
    dX.append(v0)

    return Trajectory()
