from processor import WaypointListProcessor, WaypointStreamProcessor
from utils import (load_from_json_file, convert_data_to_waypoints,
                   trip_waypoint_format)
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='extrace trips from a stream or list of Waypoints.')
    parser.add_argument('--stream', action='store_true',
                        help='extrace trips from a stream of Waypoints')
    parser.add_argument('--list', action='store_true',
                        help='extrace trips from a list of Waypoints')
    parser.add_argument('--source', dest='source',
                        help='data source file with vaild json format',
                        required=True)
    args = parser.parse_args()

    data_json = load_from_json_file(args.source)

    if isinstance(data_json, list):
        waypoints = convert_data_to_waypoints(data_json)
    else:
        print("Error: %s" % data_json)
        parser.print_help()
        exit(0)

    if args.list:
        list_processor = WaypointListProcessor(waypoints)
        trips = list_processor.get_trips()
        print(trip_waypoint_format(trips))
    elif args.stream:
        stream_processor = WaypointStreamProcessor()
        trips = [stream_processor.process_waypoint(
            waypoint) for waypoint in waypoints]
        trips = filter(None, trips)
        print(trip_waypoint_format(trips))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
