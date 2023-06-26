from typing import Union, List, Optional

import math
import numpy as np

from config import GEOMETRIC_INACCURACY


class Point:
    def __init__(self, x: Union[int, float], y: Union[int, float]) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point: x={self.x}, y={self.y}"

    def __eq__(self, other) -> bool:
        return np.isclose(self.x, other.x, atol=GEOMETRIC_INACCURACY) \
               and np.isclose(self.y, other.y, atol=GEOMETRIC_INACCURACY)


class Circle(Point):
    def __init__(self, x: Union[int, float], y: Union[int, float], r: Union[int, float]) -> None:
        self.r = abs(r)
        super().__init__(x, y)

    def __eq__(self, other) -> bool:
        if other:
            return np.isclose(self.r, other.r, atol=GEOMETRIC_INACCURACY) and self.center() == other.center()
        return False

    def __repr__(self) -> str:
        return f"Circle: x={self.x}, y={self.y}, r={self.r}"

    def center(self) -> Point:
        return Point(self.x, self.y)


class Line:
    def __init__(self, a: Union[int, float], b: Union[int, float], c: Union[int, float]) -> None:
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self) -> str:
        return f"Line: a={self.a}, b={self.b}, c={self.c}"

    def __eq__(self, other) -> bool:
        if not other:
            return False
        aspect_ratio = 1
        if other.a != 0:
            aspect_ratio = self.a / other.a
        elif other.b != 0:
            aspect_ratio = self.b / other.b
        elif other.c != 0:
            aspect_ratio = self.c / other.c
        return (np.isclose(self.a, other.a * aspect_ratio, atol=GEOMETRIC_INACCURACY)
                and np.isclose(self.b, other.b * aspect_ratio, atol=GEOMETRIC_INACCURACY)
                and np.isclose(self.c, other.c * aspect_ratio, atol=GEOMETRIC_INACCURACY))


def tangent_from_point_to_circle(point: Point, circle: Circle) -> List[Line]:
    """Строим касательную к окружности из заданной точки"""
    c = circle.center()
    lx = c.x - point.x
    ly = c.y - point.y
    l = (lx ** 2 + ly ** 2) ** 0.5
    t1x = circle.r * np.sin(np.arctan2(ly, lx) - np.arcsin(circle.r / l)) + c.x
    t1y = circle.r * -np.cos(np.arctan2(ly, lx) - np.arcsin(circle.r / l)) + c.y
    t2x = circle.r * -np.sin(np.arctan2(ly, lx) + np.arcsin(circle.r / l)) + c.x
    t2y = circle.r * np.cos(np.arctan2(ly, lx) + np.arcsin(circle.r / l)) + c.y

    t1 = Point(t1x, t1y)
    t2 = Point(t2x, t2y)
    return [
        line_by_two_points(t1, point),
        line_by_two_points(t2, point)
    ]


def points_on_line(line: Line, point: Point, distance: Union[int, float]) -> List[Point]:
    """Находит точки на прямой лежащие на расстоянии distance от исходной точки point"""
    circle = Circle(point.x, point.y, distance)
    print(crossings(line, circle))
    return crossings(line, circle)


def line_by_two_points(point1: Point, point2: Point) -> Line:
    if point1.x == point2.x:
        return Line(1, 0, -point1.x)
    else:
        a = (point1.y - point2.y) / (point2.x - point1.x)
        b = 1
        c = -(a * point1.x) - (b * point1.y)
        return Line(a, b, c)


def crossings(line: Line, circle: Circle) -> List[Point]:
    """Function finds points of intersection between circle and line"""
    # Source: https://www.cyberforum.ru/geometry/thread337902.html?ysclid=lgb8utp5z3784822414

    r = circle.r
    vec_len = (line.a ** 2 + line.b ** 2) ** 0.5  # Length of direction vector
    distance = (line.a * circle.x + line.b * circle.y + line.c) / vec_len  # circleCenter-line distance (signed)
    u_distance = abs(distance)  # circleCenter-line distance (unsigned)
    if u_distance - r > GEOMETRIC_INACCURACY / 10:  # line does not cross the circle (with little gap)
        return []
    if r < u_distance:
        r = u_distance  # calculation error override
    dir_sin = line.a / vec_len  # sine of angle between direction vector and line
    dir_cos = line.b / vec_len  # cosine of angle between direction vector and line
    xo = circle.x - distance * dir_sin  # projection of the circleCenter onto the line (x coord)
    yo = circle.y - distance * dir_cos  # projection of the circleCenter onto the line (x coord)
    half_chord_len = (r ** 2 - distance ** 2) ** 0.5  # length of the half-chord
    xs1 = xo + half_chord_len * dir_cos
    ys1 = yo - half_chord_len * dir_sin
    xs2 = xo - half_chord_len * dir_cos
    ys2 = yo + half_chord_len * dir_sin
    points = [Point(xs1, ys1), Point(xs2, ys2)]
    return points if points[0] != points[1] else points[:1]


def distance_between_point_and_line(point: Point, line: Line) -> float:
    return abs(line.a * point.x + line.b * point.y + line.c) / math.sqrt(line.a ** 2 + line.b ** 2)


def distance_between_points(point1: Point, point2: Point) -> float:
    return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** 0.5


def solve_quadratic_equation(a: Union[int, float], b: Union[int, float], c: Union[int, float]) -> Optional[List[float]]:
    if a == 0:
        return [-c / b, ]
    d = (b ** 2) - (4 * a * c)
    if d < 0:
        return []
    t1 = (-b + d ** 0.5) / (2 * a)
    t2 = (-b - d ** 0.5) / (2 * a)
    return [t1, t2] if d > 0 else [t1,]
