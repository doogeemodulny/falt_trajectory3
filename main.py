import logging

from vizualization import draw_all
from read_data import read_data
from kommivoyager import LittleSolver
from matrix_handler import MatrixHandler
from config import LOG_FILE, INPUT_FILE

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

if __name__ == '__main__':
    solver = LittleSolver()
    handler = MatrixHandler()

    filename = INPUT_FILE
    matrix_of_roads = handler.get_roads_matrix(filename)

    matrix_of_distances = handler.get_distances_from_matrix_of_roads(matrix_of_roads)
    path, record = solver.findPath(matrix_of_distances)

    data = read_data(filename)
    draw_all(path, data)
