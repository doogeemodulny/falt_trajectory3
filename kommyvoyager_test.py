import numpy as np
from kommivoyager import LittleSolver


def test_kommyvoyager():
    L = LittleSolver()
    tests = [np.array([[np.inf, 10],
                           [0, np.inf]]),
                 np.array([[np.inf, 15, 40],
                           [43, np.inf, 4],
                           [30, 5, np.inf]]),
                 np.array([[np.inf, 43, 22, 14],
                           [15, np.inf, 53, 2],
                           [23, 10, np.inf, 4],
                           [21, 67, 6, np.inf]]),
                 np.array([[np.inf, 75, 139, 34, 15],
                           [3, np.inf, 34, 12, 33],
                           [23, 43, np.inf, 11, 52],
                           [21, 0, 35, np.inf, 2],
                           [0, 0, 0, 0, np.inf]]),
                 np.array([[np.inf, 0, 0, 0, 0, 0, 0],
                           [0, np.inf, 0, 0, 0, 0, 0],
                           [0, 0, np.inf, 0, 0, 0, 0],
                           [0, 0, 0, np.inf, 0, 0, 0],
                           [0, 0, 0, 0, np.inf, 0, 0],
                           [0, 0, 0, 0, 0, np.inf, 0],
                           [0, 0, 0, 0, 0, 0, np.inf]]),
                 np.array([[np.inf, 5, 5, 5, 5, 5, 5],
                           [5, np.inf, 5, 5, 5, 5, 5],
                           [5, 5, np.inf, 5, 5, 5, 5],
                           [5, 5, 5, np.inf, 5, 5, 5],
                           [5, 5, 5, 5, np.inf, 5, 5],
                           [5, 5, 5, 5, 5, np.inf, 5],
                           [5, 5, 5, 5, 5, 5, np.inf]]),
                 np.array([[np.inf, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                           [11, np.inf, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                           [21, 22, np.inf, 23, 24, 25, 26, 27, 28, 29, 30],
                           [31, 32, 33, np.inf, 34, 35, 36, 37, 38, 39, 40],
                           [41, 42, 43, 44, np.inf, 45, 46, 47, 48, 49, 50],
                           [51, 52, 53, 54, 55, np.inf, 56, 57, 58, 59, 60],
                           [61, 62, 63, 64, 65, 66, np.inf, 67, 68, 69, 70],
                           [71, 72, 73, 74, 75, 76, 77, np.inf, 78, 79, 80],
                           [81, 82, 83, 84, 85, 86, 87, 88, np.inf, 89, 90],
                           [91, 92, 93, 94, 95, 96, 97, 98, 99, np.inf, 100],
                           [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, np.inf]])]
    test_answers = [10, 49, 45, 29, 0, 35, 606]

    for i in range(len(tests)):
        path, record = L.findPath(tests[i])
        assert record == test_answers[i]


def test_substractFromMatrix():
    L = LittleSolver()
    test_matrix = np.array([[np.inf, 1, 2],
                            [2, np.inf, 1],
                            [3, 2, np.inf]])
    result_matrix = np.array([[np.inf, 0, 1],
                            [0, np.inf, 0],
                            [0, 0, np.inf]])
    result_substractSum = 5
    assert result_substractSum, result_matrix == L.substractFromMatrix(test_matrix)


def test_getCoefficient():
    L = LittleSolver()
    test_matrix = np.array([[np.inf, 0, 1],
                            [0, np.inf, 0],
                            [0, 2, np.inf]])
    result = 3
    assert L.getCoefficient(test_matrix, 0, 1) == result


def test_pathGenerator():
    L = LittleSolver()
    test_path = [(0, 1), (3, 4), (4, 5), (5, 6), (1, 2), (2, 3), (6, 0)]
    test_begin = [2]
    result = [[2, 3, 4, 5, 6, 0, 1, 2]]
    assert L.pathGenerator(test_path, test_begin) == result


def test_getMaxCoeffElement():
    L = LittleSolver()
    test_matrix = np.array([[np.inf, 0, 1],
                            [0, np.inf, 0],
                            [0, 2, np.inf]])
    result = (0,1)
    assert L.getMaxCoeffElement(test_matrix) == result


def test_setInf():
    L = LittleSolver()
    test_matrix = np.array([[np.inf, 0, 1],
                            [0, 0, np.inf],
                            [0, 2, 0]])
    result = np.array([[np.inf, 0, 1],
                            [0, 0, np.inf],
                            [0, np.inf, 0]])
    assert (L.setInf(test_matrix) == result).all()

def test_TSP():
    L = LittleSolver()
    test_matrix = np.array([[np.inf, 1, 2],
                            [3, np.inf, 1],
                            [4, 2, np.inf]])
    path, record = L.findPath(test_matrix, planeCount=2)
    result = [[0, 2, 0], [0, 1, 0]]
    assert(path == result)


