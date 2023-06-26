import numpy as np

from abc import ABC, abstractmethod

from geometry import *
from read_data import read_data
from itertools import chain
from config import GEOMETRIC_INACCURACY, ARC_DISCRETISATION, ARC_WIDTH, LINE_WIDTH, LINE_COLOR


class RoadUpdater:
    def __init__(self):
        self.__circles = []
        self.__road = Road()
        self.__A = Point(0, 0)
        self.__B = Point(0, 0)

    def update_road(self, point1, point2):
        self.__A = point1
        self.__B = point2
        self.__make_road()
        return self.road

    @property
    def circles(self):
        return self.__circles

    def __get_circles_from_data(self, data):
        for zone in data["data_forbidden_zone"]:
            self.circles.append(Circle(zone["x"], zone["y"], zone["r"]))

    def __distances_to_circles(self, point):
        """Расстояния от точки до всех окружностей (не их центров)"""
        return [(distance_between_points(x.center(), point) - x.r) for x in self.circles]

    def __point_of_circle(self, point):
        """Возвращает список окружностей, которым принадлежит точка"""
        return [c for c in self.circles if distance_between_points(c.center(), point) < c.r + GEOMETRIC_INACCURACY]

    def __nearest_crossed_circle(self, point):
        """Находит ближайший пересеченный круг прямой через данную точку и конечную точку (self.B)"""

        lineAB = line_by_two_points(point, self.__B)  # Прямая АБ через начальную и конечную точку
        self.__get_circles_from_data(read_data("input.json"))

        # Список точек пересечения или касания прямой АБ co всеми окружностями которые она пересекает или касается
        crossing_points_with_circles = list(chain(*[crossings(lineAB, c) for c in self.circles]))
        crossing_points_with_circles = [p for p in crossing_points_with_circles
                                        if (min(point.x, self.__B.x) <= p.x <= max(point.x, self.__B.x)
                                            and min(point.y, self.__B.y) <= p.y <= max(point.y, self.__B.y))]

        # Ближайший пересеченный круг
        if crossing_points_with_circles:
            nearest_crossed_circle = self.__point_of_circle(min(crossing_points_with_circles,
                                                                key=lambda x: distance_between_points(x, point)))[0]
            return nearest_crossed_circle

    def __make_road(self):
        nc_circle = self.__nearest_crossed_circle(self.__A)
        if not nc_circle:
            road = Road()
            road.add(Segment(self.__A, self.__B))
            self.road = road
            return
        tangentials_to_nc_circle_from_A = tangent_from_point_to_circle(self.__A, nc_circle)
        tangentials_to_nc_circle_from_B = tangent_from_point_to_circle(self.__B, nc_circle)
        possible_roads = []
        for tang_a in tangentials_to_nc_circle_from_A:
            road_first_part = Road()
            touch_point_a = crossings(tang_a, nc_circle)[0]
            s1 = Segment(self.__A, touch_point_a)
            road_first_part.add(s1)

            for tang_b in tangentials_to_nc_circle_from_B:
                road_second_part = Road()
                touch_point_b = crossings(tang_b, nc_circle)[0]
                s2 = Segment(touch_point_b, self.__B)
                road_second_part.add(s2)

                a = Arc(nc_circle, touch_point_a, touch_point_b)
                road_second_part.add(a)

                whole_possible_road = road_first_part + road_second_part
                possible_roads.append(whole_possible_road)
        self.road = min(possible_roads, key=lambda x: x.length)


class Road:
    def __init__(self):
        self.__parts = []
        self.__length = 0

    def __eq__(self, other):
        if other:
            return (len(self.parts) == len(other.parts)
                    and set(self.parts) == set(other.parts))
        return False

    def __repr__(self):
        string_representation = ""
        for x in self.parts:
            string_representation += str(x)
        return string_representation

    def __add__(self, other):
        r = Road()
        all_parts = self.parts + other.parts
        for part in all_parts:
            r.add(part)
        return r

    def __hash__(self):
        r_hash = 1
        for p in self.parts:
            r_hash *= hash(p)
        return r_hash

    def add(self, road_part):
        self.parts.append(road_part)
        self.__length += road_part.length

    @property
    def parts(self):
        return self.__parts

    @property
    def length(self):
        return self.__length

    def draw(self, ax):
        for part in self.parts:
            part.draw(ax)


class RoadPart(ABC):
    @abstractmethod
    def draw(self, ax):
        pass

    @property
    @abstractmethod
    def length(self):
        pass


class Segment(RoadPart):
    def __init__(self, point1: Point, point2: Point):
        self.pointStart = point1
        self.pointFinish = point2
        self.__length = 0
        self.__calc_length()

    def __repr__(self):
        return f"Segment[{self.pointStart} : {self.pointFinish}]"

    def __eq__(self, other):
        if other:
            return self.pointStart == other.pointStart and self.pointFinish == other.pointFinish
        return False

    def __hash__(self):
        return (131 * int(self.pointStart.x * 10 ** 6) * 149 * int(self.pointStart.y * 10 ** 6) *
                157 * int(self.pointFinish.x * 10 ** 6) * 181 * int(self.pointFinish.y * 10 ** 6))

    @property
    def length(self):
        return self.__length

    def __calc_length(self):
        self.__length = ((self.pointStart.x - self.pointFinish.x) ** 2 + (
                self.pointStart.y - self.pointFinish.y) ** 2) ** 0.5

    def draw(self, ax):
        x = np.array((self.pointStart.x, self.pointFinish.x), dtype=np.float64)
        y = np.array((self.pointStart.y, self.pointFinish.y), dtype=np.float64)
        ax.plot(x, y, color=LINE_COLOR, lw=LINE_WIDTH)


class Arc(RoadPart):
    def __init__(self, circle, point1: Point, point2: Point):
        self.circle = circle
        self.pointStart = point1
        self.pointFinish = point2
        self.__length = 0
        self.__calc_length()

    def __repr__(self):
        return f"Arc center{self.circle.center()}, radius={self.circle.r}, " \
               f"startPoint={self.pointStart}, finishPoint={self.pointFinish}"

    def __eq__(self, other):
        return self.circle == other.circle and self.pointStart == other.pointStart \
               and self.pointFinish == other.pointFinish

    def __hash__(self):
        return (13 * int(self.circle.r * 10 ** 6) * 17 * int(self.circle.x * 10 ** 6) * 43 * int(
            self.circle.y * 10 ** 6) +
                61 * int(self.pointStart.x * 10 ** 6) * 79 * int(self.pointStart.y * 10 ** 6) *
                97 * int(self.pointFinish.x * 10 ** 6) * 101 * int(self.pointFinish.y * 10 ** 6))

    def draw(self, ax):
        alpha = np.arctan2((self.pointStart.y - self.circle.y), (self.pointStart.x - self.circle.x))
        beta = np.arctan2((self.pointFinish.y - self.circle.y), (self.pointFinish.x - self.circle.x))
        arc_angles = np.linspace(alpha, beta, ARC_DISCRETISATION)
        arc_xs = self.circle.x + self.circle.r * np.cos(arc_angles)
        arc_ys = self.circle.y + self.circle.r * np.sin(arc_angles)
        ax.plot(arc_xs, arc_ys, color=LINE_COLOR, lw=ARC_WIDTH)

    @property
    def length(self):
        return self.__length

    def __calc_length(self):
        half_chord = 0.5 * (((self.pointStart.x - self.pointFinish.x) ** 2 +
                             (self.pointStart.y - self.pointFinish.y) ** 2) ** 0.5)
        angle = np.arcsin(half_chord / self.circle.r) * 2
        self.__length = 2 * np.pi * self.circle.r * angle / (2 * np.pi)
