import pytest
from processor import (WaypointListProcessor, Waypoint,
                       Trip, WaypointStreamProcessor)
from tests.fixtures import (FixtureTestWaypointStreamProcessor,
                            FixtureTestWaypointListProcessor)


class TestWaypointListProcessor(FixtureTestWaypointListProcessor):

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

    def test_list_without_stoping_point(self):
        list_processor = WaypointListProcessor(
            self.waypoints_list_without_stoping_point)
        assert list_processor.get_trips() == [
            Trip(
                distance=567954.0964794011,
                start=Waypoint(timestamp='2018-08-10T20:10:22Z',
                               lat=54.54987, lng=12.41039),
                end=Waypoint(timestamp='2018-08-10T20:22:22Z',
                             lat=59.64987, lng=12.41039)
            )]

    def test_list_with_two_trips(self):
        list_processor = WaypointListProcessor(
            self.waypoints_list_with_two_trips)
        assert list_processor.get_trips() == [
            Trip(distance=222593.124196202,
                 start=Waypoint(timestamp='2018-08-10T20:04:22Z',
                                lat=52.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:06:22Z',
                              lat=54.54987, lng=12.41039)
                 ),
            Trip(distance=556802.4117352704,
                 start=Waypoint(timestamp='2018-08-10T20:10:22Z',
                                lat=54.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:17:22Z',
                              lat=59.54987, lng=12.41039)
                 )
        ]

    def test_list_starts_with_not_moving_points(self):
        # List beginning with same points, which means that
        # the car has not moved yet
        list_processor = WaypointListProcessor(
            self.waypoints_list_starts_with_not_moving_points)
        assert list_processor.get_trips() == [
            Trip(distance=779395.5359314724,
                 start=Waypoint(timestamp='2018-08-10T20:10:22Z',
                                lat=52.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:17:22Z',
                              lat=59.54987, lng=12.41039)
                 )]

    def test_list_with_distance_less_15m(self):
        list_processor = WaypointListProcessor(
            self.waypoints_list_with_distance_less_15m)
        assert list_processor.get_trips() == []


class TestWaypointStreamProcessor(FixtureTestWaypointStreamProcessor):

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

    def test_stream_with_one_trip(self):
        stream_processor = WaypointStreamProcessor()
        results = []
        for waypoint in self.waypoints_stream_with_one_trip:
            results.append(stream_processor.process_waypoint(waypoint))
        assert results == [
            None, None, None, None,
            Trip(distance=556802.4117352711,
                 start=Waypoint(timestamp='2018-08-10T20:10:22Z',
                                lat=54.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:16:22Z',
                              lat=59.54987, lng=12.41039)
                 )]

    def test_stream_starts_with_not_moving_points(self):
        stream_processor = WaypointStreamProcessor()
        results = []
        for waypoint in self.waypoints_stream_starts_with_not_moving_points:
            results.append(stream_processor.process_waypoint(waypoint))
        assert results == [
            None, None, None, None, None, None, None, None,
            Trip(distance=556802.4117352706,
                 start=Waypoint(timestamp='2018-08-10T20:16:22Z',
                                lat=54.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:24:22Z',
                              lat=59.54987, lng=12.41039)
                 )]

    def test_stream_with_two_trips(self):
        stream_processor = WaypointStreamProcessor()
        results = []
        for waypoint in self.waypoints_stream_with_two_trips:
            results.append(stream_processor.process_waypoint(waypoint))
        assert results == [
            None, None, None, None, None, None,
            Trip(distance=445406.4349099722,
                 start=Waypoint(timestamp='2018-08-10T20:15:22Z',
                                lat=54.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:23:22Z',
                              lat=58.54987, lng=12.41039)
                 ),
            None, None,
            Trip(distance=222809.0972828272,
                 start=Waypoint(timestamp='2018-08-10T20:29:22Z',
                                lat=58.54987, lng=12.41039),
                 end=Waypoint(timestamp='2018-08-10T20:31:22Z',
                              lat=60.54987, lng=12.41039)
                 )]
