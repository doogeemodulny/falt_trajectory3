import numpy as np
import json
import logging

from roadupdater import RoadUpdater
from geometry import Point
from config import INFINITY


class MatrixHandler:
    def __init__(self):
        self.__data = {}
        self.__simple_matrix = np.array([])
        self.__marked_matrix = np.array([])
        self.__matrix_without_forbidden_lines = np.array([])
        self.__matrix_of_roads = []

    def get_distances_matrix(self, filename):
        """Interface method for getting distance matrix from json file"""
        self.__extract_data(filename)
        self.__remove_forbidden_lines()
        return self.__matrix_without_forbidden_lines

    def get_roads_matrix(self, filename):
        self.__extract_data(filename)
        self.__remove_forbidden_lines()
        self.__radars_bypass()
        return self.__matrix_of_roads

    ###########################################################

    def __extract_data(self, filename):
        """ Extracting data from json file """

        with open(filename) as f:
            data = json.load(f)
        self.__data = data
        logging.info("Прочитали данные")

    @staticmethod
    def __distance(point1, point2):
        """Calculates distance between point1 and point2"""

        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    def __simple_distance_matrix(self):
        """Creates matrix of distances between points without regard to forbidden zones, lines and relief"""

        points = self.__data["data_points"]
        p_quantity = len(points)
        matrix = np.full((p_quantity, p_quantity), np.Inf)
        for i in range(p_quantity):
            for j in range(p_quantity):
                if i > j:
                    continue
                d = self.__distance((points[i]["x"], points[i]["y"]),
                                    (points[j]["x"], points[j]["y"]))
                if i != j:
                    matrix[i, j] = d
                    matrix[j, i] = d
        self.__simple_matrix = matrix
        logging.info("Создали матрицу расстояний")

    def __mark_matrix_by_point_ids(self):
        """Inserts point ids as first raw and column of the matrix"""
        self.__simple_distance_matrix()
        id_row = [x["id"] for x in self.__data["data_points"]]
        id_column = np.array([0] +
                             [x["id"] for x in self.__data["data_points"]])[:, np.newaxis]
        matrix = np.vstack([id_row, self.__simple_matrix])
        matrix = np.hstack([id_column, matrix])
        self.__marked_matrix = matrix
        logging.info("Помечаем каждый столбец и строчку id соответствующей точки")

    def __remove_forbidden_lines(self):
        """Sets distance of forbidden lines as np.inf"""
        self.__mark_matrix_by_point_ids()
        forbidden_lines = [(x["id1"], x["id2"]) for x in self.__data["forbidden_lines"]]
        forbidden_lines_x = [x[0] for x in forbidden_lines]
        forbidden_lines_y = [x[1] for x in forbidden_lines]
        matrix = self.__marked_matrix
        for (x, y), value in np.ndenumerate(matrix):
            if int(matrix[x, 0]) in forbidden_lines_x \
                    and int(matrix[0, y]) in forbidden_lines_y:
                matrix[x, y] = INFINITY
                matrix[y, x] = INFINITY
        self.__matrix_without_forbidden_lines = matrix
        logging.info("Удалили запрещенные воздушные коридоры")

    ##################################################
    def __radars_bypass(self):
        """Эта функция будет обновлять матрицу расстояний"""
        matrix = self.__matrix_without_forbidden_lines
        self.__matrix_of_roads = np.empty(matrix.shape, dtype=object)

        for i in range(1, matrix.shape[0]):
            for j in range(1, matrix.shape[1]):
                if i > j or matrix[i, j] > (INFINITY - 1):
                    continue

                point1_x = [p["x"] for p in self.__data["data_points"]
                            if p["id"] == matrix[i, 0]][0]
                point1_y = [p["y"] for p in self.__data["data_points"]
                            if p["id"] == matrix[i, 0]][0]
                point2_x = [p["x"] for p in self.__data["data_points"]
                            if p["id"] == matrix[0, j]][0]
                point2_y = [p["y"] for p in self.__data["data_points"]
                            if p["id"] == matrix[0, j]][0]

                road = self.__update_road(Point(point1_x, point1_y), Point(point2_x, point2_y))
                self.__matrix_of_roads[i, j] = road
                self.__matrix_of_roads[j, i] = road

    @staticmethod
    def __update_road(point1, point2):
        """Эта функция будет возвращать объект Road - путь между двумя точками, учитывая облёт препятствий"""
        updater = RoadUpdater()
        updated_road = updater.update_road(point1, point2)
        return updated_road

    @staticmethod
    def get_distances_from_matrix_of_roads(matrix_of_roads):
        """Делаем из матрицы дорог матрицу расстояний"""
        dist_matrix = np.full((matrix_of_roads.shape[0] - 1,
                               matrix_of_roads.shape[1] - 1),
                              fill_value=INFINITY, dtype=np.float64)
        for i in range(1, matrix_of_roads.shape[0]):
            for j in range(1, matrix_of_roads.shape[1]):
                if i == j:  # если диагональный элемент
                    dist_matrix[i - 1, j - 1] = np.inf
                    continue
                if not matrix_of_roads[i, j]:  # запретный коридор
                    continue
                dist_matrix[i - 1, j - 1] = matrix_of_roads[i, j].length
        return dist_matrix
