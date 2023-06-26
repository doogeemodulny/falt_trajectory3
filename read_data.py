import json


def read_data(filename):
    """ Extracting data from json file """
    with open(filename) as f:
        data = json.load(f)
    return data
