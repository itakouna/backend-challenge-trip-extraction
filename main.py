from processor import WaypointListProcessor
from utils import load_from_json_file, convert_data_to_waypoints

data_json = load_from_json_file('data/waypoints.json')
waypoints = convert_data_to_waypoints(data_json)
list_processor = WaypointListProcessor(waypoints)
print(list_processor.get_trips())
