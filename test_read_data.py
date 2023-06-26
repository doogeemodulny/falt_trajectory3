from read_data import read_data
from config import TEST_READ_DATA_FILE


def test_read_data():
    d = {
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

    assert read_data(TEST_READ_DATA_FILE) == d