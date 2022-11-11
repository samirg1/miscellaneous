#!/usr/bin/env python3
from math import pi, sqrt, acos

def euclidean_distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


def circle_contains(cx, cy, r, x, y):
    return euclidean_distance(cx, cy, x, y) <= r


def circle_contains2(c, r, p):
    return euclidean_distance(c[0], c[1], p[0], p[1]) <= r


def circles_intersect(cx1, cy1, r1, cx2, cy2, r2):
    return euclidean_distance(cx1, cy1, cx2, cy2) <= r1 + r2


def circles_intersect2(c1, r1, c2, r2):
    return euclidean_distance(c1[0], c1[1], c2[0], c2[1]) <= r1 + r2


def circles_intersect3(c1, c2):
    return euclidean_distance(c1.centre[0], c1.centre[1], c2.centre[0], c2.centre[1]) <= c1.radius + c2.radius


class Circle:
    """
    Represents a circle of certain radius around some centre.
    """

    def __init__(self, centre=(0.0, 0.0), radius=1.0):
        self.centre = centre
        self.radius = radius

    def __repr__(self):
        return 'Circle({}, {})'.format(self.centre, self.radius)

    def circumference(self):
        return 2*self.radius*pi

    def diameter(self):
        return 2*self.radius

    def area(self):
        return pi * self.radius**2

    def contains_point(self, point):
        max_x = self.centre[0] + self.radius
        min_x = self.centre[0] - self.radius
        max_y = self.centre[1] + self.radius
        min_y = self.centre[1] - self.radius
        return point[0] < max_x and point[0] > min_x and point[1] > min_y and point[1] < max_y

    def intersects(self, other):
        return (self.centre[0]-other.centre[0])**2 + (self.centre[1]-other.centre[1])**2 < (self.radius + other.radius)**2


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector({}, {})'.format(self.x, self.y)

    def norm(self):
        return sqrt((self.x)**2 + (self.y)**2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cosine(self, other):
        return acos(self.dot(other) / (self.norm()*other.norm()))*180/pi

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(scalar*self.x, scalar*self.y)

    def __truediv__(self, scalar):
        return Vector(self.x/scalar, self.y/scalar)

    def __rmul__(self, scalar):
        return Vector(scalar*self.x, scalar*self.y)

    def projection(self, other):
        return other.dot(self) / other.dot(other) * other


class Triangle:

    def __init__(self, a, b, c):
        self.a = Vector(a[0], a[1])
        self.b = Vector(b[0], b[1])
        self.c = Vector(c[0], c[1])

    def __repr__(self):
        return 'Triangle({}, {}, {})'.format((self.a.x, self.a.y), (self.b.x, self.b.y), (self.c.x, self.c.y))

    def area(self):
        base = self.c - self.a
        length_base = base.norm()
        point = self.a + (self.b - self.a).projection(base)
        alt = (self.b - point).norm()
        return alt * length_base / 2