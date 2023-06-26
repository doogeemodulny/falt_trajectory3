import numpy as np
from geometry import *


def test_solve_quadratic_equation():
    assert solve_quadratic_equation(1, 1, 1) == []
    assert np.isclose(solve_quadratic_equation(2, -10, 4)[0], 4.56155281)
    assert np.isclose(solve_quadratic_equation(2, -10, 4)[1], 0.43844718)
    assert np.isclose(solve_quadratic_equation(2, 7, 3)[0], -0.5)
    assert np.isclose(solve_quadratic_equation(2, 7, 3)[1], -3)
    assert np.isclose(solve_quadratic_equation(3, 6, 3)[0], -1.0)


def test_distance_between_points():
    point1 = Point(0, -1)
    point2 = Point(4, 0)
    point3 = Point(3, 3)
    point4 = Point(17, -4)
    point5 = Point(17, 0)
    assert distance_between_points(point1, point3) == 5
    assert distance_between_points(point4, point5) == 4
    assert distance_between_points(point2, point5) == 13
    assert np.isclose(distance_between_points(point1, point4), 17.2626765)
    assert np.isclose(distance_between_points(point3, point4), 15.65247)


def test_distance_between_point_and_line():
    point0 = Point(2, 2)
    point1 = Point(4, 14.8)
    point2 = Point(-7, 23)
    point3 = Point(12, -8)
    line0 = Line(1, -1, 0)
    line1 = Line(0, 6.9, 8)
    line2 = Line(12, -6.9, 85)
    line3 = Line(9, 14.796, 0)
    line4 = Line(5, 0, 2.77)

    assert np.isclose(distance_between_point_and_line(point0, line0), 0)
    assert np.isclose(distance_between_point_and_line(point1, line0), 7.636753)
    assert np.isclose(distance_between_point_and_line(point1, line1), 15.95942)
    assert np.isclose(distance_between_point_and_line(point2, line3), 16.0124768)
    assert np.isclose(distance_between_point_and_line(point3, line4), 12.554)
    assert np.isclose(distance_between_point_and_line(point3, line2), 20.531230)
    assert np.isclose(distance_between_point_and_line(point2, line2), 11.3925936)


def test_crossings():
    line1 = Line(2, 0, -4)
    line2 = Line(0, 3, -6)
    line3 = Line(12, 3, 4)
    circle1 = Circle(0, 0, 2)
    circle2 = Circle(4, 4, 2)
    circle3 = Circle(10, 1, 12)

    assert crossings(line1, circle1) == [Point(2, 0)]
    assert crossings(line1, circle2) == [Point(2, 4)]
    assert crossings(line2, circle1) == [Point(0, 2)]
    assert crossings(line2, circle2) == [Point(4, 2)]
    assert (crossings(line3, circle1) == [Point(-0.7924139, 1.836322), Point(0.16496296, -1.993185)]) \
           or (crossings(line3, circle1) == [Point(0.16496296, -1.993185), Point(-0.7924139, 1.836322)])
    assert (crossings(line3, circle3) == [Point(-1.467274, 4.53576339), Point(1.545705, -7.5161555)]) \
           or (crossings(line3, circle3) == [Point(1.545705, -7.5161555), Point(-1.467274, 4.53576339)])
    assert (crossings(line2, circle3) == [Point(-1.9582607, 2), Point(21.9582607, 2)]) \
           or (crossings(line2, circle3) == [Point(21.9582607, 2), Point(-1.9582607, 2)])


def test_line_by_two_points():
    point1 = Point(2, 3)
    point2 = Point(-6, 3)
    point3 = Point(-6, 0)
    point4 = Point(-1, 1.3541666)
    point5 = Point(0.18181818, 0)
    point6 = Point(4.643, 16.0718)
    point7 = Point(-2.11475769, -1.49837)
    point8 = Point(2.19384, -2.3432307)
    point9 = Point(2.9185104, 1.83756)

    assert line_by_two_points(point1, point2) == Line(0, 1, -3)
    assert line_by_two_points(point3, point2) == Line(1, 0, 6)
    assert Line(1.1458332, 1, -0.208333) == Line(11, 9.6, -2)
    assert line_by_two_points(point4, point5) == Line(11, 9.6, -2)
    assert line_by_two_points(point6, point7) == Line(13, -5, 20)
    assert line_by_two_points(point8, point9) == Line(-3, 0.52, 7.8)


def test_points_on_line():
    line1 = Line(1, 3, 0)
    line2 = Line(1.5, 0, 4)
    line3 = Line(0, 2.3, 4.7)
    point1 = Point(-2.66666, 0.88888)
    point2 = Point(-2.666666, -2.043478)
    point3 = Point(6.1304347, -2.043478)
    dist1 = 4
    dist2 = 15.7
    dist3 = 6.905

    assert points_on_line(line1, point1, dist1) == [Point(1.128, -0.376), Point(-6.461, 2.153)] \
           or points_on_line(line1, point1, dist1) == [Point(-6.461, 2.153), Point(1.128, -0.376)]
    assert points_on_line(line2, point2, dist2) == [Point(-2.667, 13.657), Point(-2.667, -17.743)] \
           or points_on_line(line2, point2, dist2) == [Point(-2.667, -17.743), Point(-2.667, 13.657)]
    assert points_on_line(line3, point3, dist3) == [Point(-0.775, -2.043), Point(13.035, -2.043)] \
           or points_on_line(line3, point3, dist3) == [Point(13.035, -2.043), Point(-0.775, -2.043)]


def test_tangent_from_point_to_circle():
    point1 = Point(0, 0)
    point2 = Point(12.46813, 9.98956)
    circle1 = Circle(19.95, 0, 6.31)
    circle2 = Circle(0, -4.9, 4.65)
    circle3 = Circle(14, -3, 12)
    line1 = Line(1, 3, 0)
    line2 = Line(1, -3, 0)
    line3 = Line(3.60388, -6.2, 17.0016)
    line4 = Line(-1.5016, -5, 68.6704)
    assert tangent_from_point_to_circle(point1, circle1) == [line1, line2] \
           or tangent_from_point_to_circle(point1, circle1) == [line2, line1]
    assert tangent_from_point_to_circle(point1, circle2) == [line1, line2] \
           or tangent_from_point_to_circle(point1, circle2) == [line2, line1]
    assert tangent_from_point_to_circle(point2, circle3) == [line3, line4] \
           or tangent_from_point_to_circle(point2, circle3) == [line4, line3]
