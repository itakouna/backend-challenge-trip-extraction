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
