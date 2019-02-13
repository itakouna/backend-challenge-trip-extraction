from processor import WaypointListProcessor, Waypoint
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
