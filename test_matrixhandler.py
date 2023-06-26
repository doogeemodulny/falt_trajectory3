import numpy as np
from matrix_handler import MatrixHandler

handler = MatrixHandler()


def test_extracting_data():
    expected_data = {
        "n": 1,
        "data_points": [
            {
                "id": 0,
                "x": 0,
                "y": 0
            },
            {
                "id": 1001,
                "x": 30,
                "y": 40
            },
            {
                "id": 1002,
                "x": 80,
                "y": 80
            }
        ],
        "forbidden_lines": [
            {
                "id1": 1001,
                "id2": 1002
            }
        ]
    }
    handler._MatrixHandler__extract_data("test_read_data.json")
    assert expected_data == handler._MatrixHandler__data


def test_distance():
    assert MatrixHandler._MatrixHandler__distance((20, 30), (50, 70)) == 50


def test_simple_distance_matrix():
    handler._MatrixHandler__extract_data("test_read_data.json")
    handler._MatrixHandler__simple_distance_matrix()
    expected_matrix = np.array([[np.inf, 50, 113.13708499],
                                [50, np.inf, 64.0312423743],
                                [113.13708499, 64.0312423743, np.inf]])
    assert np.allclose(expected_matrix, handler._MatrixHandler__simple_matrix)


def test_marked_matrix():
    handler._MatrixHandler__extract_data("test_read_data.json")
    handler._MatrixHandler__simple_distance_matrix()
    handler._MatrixHandler__mark_matrix_by_point_ids()
    expected_matrix = np.array([[0, 0, 1001, 1002],
                                [0, np.inf, 50, 113.13708499],
                                [1001, 50, np.inf, 64.0312423743],
                                [1002, 113.13708499, 64.0312423743, np.inf]])
    assert np.allclose(expected_matrix, handler._MatrixHandler__marked_matrix)


def test_remove_forbidden_lines():
    handler._MatrixHandler__extract_data("test_read_data.json")
    handler._MatrixHandler__simple_distance_matrix()
    handler._MatrixHandler__mark_matrix_by_point_ids()
    handler._MatrixHandler__remove_forbidden_lines()
    expected_matrix = np.array([[0, 0, 1001, 1002],
                                [0, np.inf, 50, 113.13708499],
                                [1001, 50, np.inf, 1e32],
                                [1002, 113.13708499, 1e32, np.inf]])
    assert np.allclose(expected_matrix, handler._MatrixHandler__matrix_without_forbidden_lines)
