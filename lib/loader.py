import json

from processor import Waypoint


def load_from_json_file(file_path):
    with open(file_path) as _file:
        return json.load(_file)


def convert_data_to_waypoints(data_points):
    return [Waypoint(**point) for point in data_points]
