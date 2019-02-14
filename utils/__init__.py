import json

from processor import Waypoint


def load_from_json_file(file_path):
    try:
        with open(file_path) as _file:
            return json.load(_file)
    except FileNotFoundError:
        return "There is no file: %s" % file_path
    except json.decoder.JSONDecodeError:
        return "The file %s has invaild json format" % file_path


def convert_data_to_waypoints(data_points):
    return [Waypoint(**point) for point in data_points]


def trip_waypoint_format(data_points):
    return [{
        "start": {
            "timestamp": point.start.timestamp,
            "lat": point.start.lat,
            "lng": point.start.lng,
        }, "end": {
            "timestamp": point.end.timestamp,
            "lat": point.end.lat,
            "lng": point.end.lng,
        },
        "distance": point.distance
    } for point in data_points]
