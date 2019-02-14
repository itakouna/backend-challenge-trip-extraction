from processor import WaypointListProcessor, Waypoint, Trip
from utils import trip_waypoint_format
import pytest


class TestProcessor():

    @pytest.mark.parametrize("current_point, next_point, expected", [
        (Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039),
         Waypoint("2018-08-10T20:04:22Z", 51.54987, 12.41039), True),
        (Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039),
         Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039), False)
    ])
    def test_car_on_move(self, current_point, next_point, expected):
        list_processor = WaypointListProcessor([])
        assert list_processor._car_in_move(
            current_point, next_point) == expected

    @pytest.mark.parametrize("points, expected", [
        # stop for 2 mintues
        ([Waypoint("2018-08-10T20:04:22Z", 51.54987, 12.41039),
          Waypoint("2018-08-10T20:06:22Z", 51.54987, 12.41039)], False),
        # points with 1 point
        ([Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039)], False),
        # stop for more than 3 mintues
        ([Waypoint("2018-08-10T20:04:22Z", 51.54987, 12.41039),
          Waypoint("2018-08-10T20:10:22Z", 51.54987, 12.41039)], True),
    ])
    def test_car_trip_has_ended(self, points, expected):
        list_processor = WaypointListProcessor([])
        assert list_processor._car_trip_has_ended(points) == expected

    def test_get_trip_for_with_non_stop_point(self):
        waypoints = [Waypoint("2018-08-10T20:10:22Z", 54.54987, 12.41039),
                     Waypoint("2018-08-10T20:15:22Z", 57.54987, 12.41039),
                     Waypoint("2018-08-10T20:16:22Z", 58.54987, 12.41039),
                     Waypoint("2018-08-10T20:17:22Z", 59.54987, 12.41039),
                     Waypoint("2018-08-10T20:22:22Z", 59.64987, 12.41039)
                     ]
        list_processor = WaypointListProcessor(waypoints)
        assert list_processor.get_trips() == [
            Trip(
                distance=567942.9577481565,
                start=Waypoint(timestamp='2018-08-10T20:10:22Z',
                               lat=54.54987, lng=12.41039),
                end=Waypoint(timestamp='2018-08-10T20:22:22Z',
                             lat=59.64987, lng=12.41039))]

    def test_get_trip_with_two_trips(self):
        waypoints = [
            Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039),
            Waypoint("2018-08-10T20:06:22Z", 54.54987, 12.41039),
            Waypoint("2018-08-10T20:08:22Z", 54.54987, 12.41039),
            Waypoint("2018-08-10T20:10:22Z", 54.54987, 12.41039),
            Waypoint("2018-08-10T20:15:22Z", 57.54987, 12.41039),
            Waypoint("2018-08-10T20:16:22Z", 58.54987, 12.41039),
            Waypoint("2018-08-10T20:17:22Z", 59.54987, 12.41039),
            Waypoint("2018-08-10T20:22:22Z", 59.54987, 12.41039)
        ]
        list_processor = WaypointListProcessor(waypoints)
        assert list_processor.get_trips() == [
            Trip(distance=222593.12419555362,
                 start=Waypoint(timestamp='2018-08-10T20:04:22Z',
                                lat=52.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:06:22Z',
                              lat=54.54987, lng=12.41039)),
            Trip(distance=556802.4117337333,
                 start=Waypoint(timestamp='2018-08-10T20:10:22Z',
                                lat=54.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:17:22Z',
                              lat=59.54987, lng=12.41039))
        ]

    def test_get_trip_with_list_beginning_with_same_points(self):
        # List beginning with same points, which means that
        # the car has not moved yet
        waypoints = [
            Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039),
            Waypoint("2018-08-10T20:06:22Z", 52.54987, 12.41039),
            Waypoint("2018-08-10T20:08:22Z", 52.54987, 12.41039),
            Waypoint("2018-08-10T20:10:22Z", 52.54987, 12.41039),
            Waypoint("2018-08-10T20:15:22Z", 57.54987, 12.41039),
            Waypoint("2018-08-10T20:16:22Z", 58.54987, 12.41039),
            Waypoint("2018-08-10T20:17:22Z", 59.54987, 12.41039),
            Waypoint("2018-08-10T20:18:22Z", 59.54987, 12.41039)
        ]
        list_processor = WaypointListProcessor(waypoints)
        assert list_processor.get_trips() == [
            Trip(distance=779395.5359292869,
                 start=Waypoint(timestamp='2018-08-10T20:10:22Z',
                                lat=52.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:17:22Z', lat=59.54987, lng=12.41039))]

    def test_get_trip_distance_less_15m(self):
        waypoints = [
            Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039),
            Waypoint("2018-08-10T20:06:22Z", 52.54987, 12.41031),
            Waypoint("2018-08-10T20:10:22Z", 52.54991, 12.41036)
        ]
        list_processor = WaypointListProcessor(waypoints)
        assert list_processor.get_trips() == []

    def test_get_trip_distance_more_15m(self):
        waypoints = [
            Waypoint("2018-08-10T20:04:22Z", 52.54987, 12.41039),
            Waypoint("2018-08-10T20:06:22Z", 52.54989, 12.41039),
            Waypoint("2018-08-10T20:10:22Z", 52.55998, 12.41039)
        ]
        list_processor = WaypointListProcessor(waypoints)
        assert list_processor.get_trips() == [
            Trip(distance=1125.0192831925704,
                 start=Waypoint(timestamp='2018-08-10T20:04:22Z',
                                lat=52.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:10:22Z',
                              lat=52.55998, lng=12.41039))]
