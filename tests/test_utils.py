from processor import Waypoint, Trip
from utils import trip_waypoint_format


class TestUtils():

    def test_trip_waypoint_format(self):
        data_points = [
            Trip(
                distance=1125.0192831925704,
                start=Waypoint(timestamp='2018-08-10T20:04:22Z',
                               lat=52.54987, lng=12.41039),
                end=Waypoint(timestamp='2018-08-10T20:10:22Z',
                             lat=52.55998, lng=12.41039)
            )
        ]
        expected_result = [
            {
                'start':
                {
                    'timestamp': '2018-08-10T20:04:22Z',
                    'lat': 52.54987, 'lng': 12.41039
                },
                'end': {
                    'timestamp': '2018-08-10T20:10:22Z',
                    'lat': 52.55998, 'lng': 12.41039
                },
                'distance': 1125.0192831925704
            }
        ]
        assert trip_waypoint_format(data_points) == expected_result
