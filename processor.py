from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Union, NamedTuple, Tuple
from lib.geo import GeoAdapter, GeopyLibrary


class Waypoint(NamedTuple):
    timestamp: datetime
    lat: float
    lng: float


class Trip(NamedTuple):
    distance: int
    start: Waypoint
    end: Waypoint


class ListProcessor(metaclass=ABCMeta):
    def __init__(self, waypoints: Tuple[Waypoint]):
        """
        On initialization the ListProcessor receives the full list of all
        waypoints. This list is held in memory, so the ListProcessor has access
        to the whole list of waypoints at all time during the trip extraction
        process.

        :param waypoints: Tuple[Waypoint]
        """
        self._waypoints = waypoints

    @abstractmethod
    def get_trips(self) -> Tuple[Trip]:
        """
        This function returns a list of Trips, which is derived from
        the list of waypoints, passed to the instance on initialization.
        """
        ...


class StreamProcessor(metaclass=ABCMeta):
    @abstractmethod
    def process_waypoint(self, waypoint: Waypoint) -> Union[Trip, None]:
        """
        Instead of a list of Waypoints, the StreamProcessor only receives one
        Waypoint at a time. The processor does not have access to the full list
        of waypoints.
        If the stream processor recognizes a complete trip, the processor
        returns a Trip object, otherwise it returns None.

        :param waypoint: Waypoint
        """
        ...


class WaypointStreamProcessor(StreamProcessor):
    STOP_TIME_IN_MINTUES = 3
    DISTANCE_SHOULD_BE_IGNORED_METERS = 15

    def __init__(self):
        self._geo = GeoAdapter(GeopyLibrary())
        self.stop_points = []
        self.move_points = []
        self.current_point = None
        self.next_point = None
        self.distance = 0.0
        self.trip = None

    def _car_in_move(self,
                     current_point: Waypoint, next_point: Waypoint) -> bool:
        return (current_point.lat != next_point.lat or
                current_point.lng != next_point.lng)

    def _car_trip_has_ended(self, stop_points: Waypoint) -> bool:
        if len(stop_points) < 2:
            return False

        time_difference = datetime.strptime(
            stop_points[-1].timestamp, "%Y-%m-%dT%H:%M:%SZ") - \
            datetime.strptime(
            stop_points[0].timestamp, "%Y-%m-%dT%H:%M:%SZ")
        return time_difference.total_seconds()/60 > self.STOP_TIME_IN_MINTUES

    def process_waypoint(self, waypoint: Waypoint) -> Union[Trip, None]:
        self.trip = None

        if not any([self.current_point, self.next_point]):
            self.next_point = waypoint
            self.current_point = waypoint
        else:
            self.current_point = self.next_point
            self.next_point = waypoint

        self.distance += self._geo.compute_distance_in_meters(
            self.current_point, self.next_point)

        if self._car_in_move(self.current_point, self.next_point):
            # only keep the last two point
            self.move_points = self.move_points[:2]
            self.move_points.extend([self.current_point, self.next_point])

        elif len(self.move_points) != 0:
            # if car had moved before it has stopped
            self.stop_points = self.stop_points[:2]
            self.stop_points.extend([self.current_point, self.next_point])

        if self._car_trip_has_ended(self.stop_points):
            # only add a trip with total distance >= 15 meters
            # the start and end point should not be the same
            if (self.distance >= self.DISTANCE_SHOULD_BE_IGNORED_METERS):
                start_point = self.move_points[0]
                end_point = self.move_points[-1]
                self.trip = Trip(
                    round(self.distance, 3), start_point, end_point)

            # Starting next trip
            # The last stop point should be the begining of the next trip
            self.move_points = self.stop_points[-1:]
            self.stop_points = []
            self.distance = 0.0
        return self.trip


class WaypointListProcessor(ListProcessor):
    STOP_TIME_IN_MINTUES = 3
    DISTANCE_SHOULD_BE_IGNORED_METERS = 15

    def __init__(self, waypoints):
        self._geo = GeoAdapter(GeopyLibrary())
        super().__init__(waypoints)

    def _car_in_move(self,
                     current_point: Waypoint, next_point: Waypoint) -> bool:
        return (current_point.lat != next_point.lat or
                current_point.lng != next_point.lng)

    def _last_value_in_list(self,
                            next_point: Waypoint,
                            last_point: Waypoint) -> bool:
        return next_point == last_point

    def _car_trip_has_ended(self, stop_points: Waypoint) -> bool:
        if len(stop_points) < 2:
            return False

        time_difference = datetime.strptime(
            stop_points[-1].timestamp, "%Y-%m-%dT%H:%M:%SZ") - \
            datetime.strptime(
            stop_points[0].timestamp, "%Y-%m-%dT%H:%M:%SZ")
        return time_difference.total_seconds()/60 > self.STOP_TIME_IN_MINTUES

    def get_trips(self) -> Tuple[Trip]:
        trips = []
        stop_points = []
        move_points = []
        distance = 0
        current_point = self._waypoints[0]
        last_point = self._waypoints[-1]

        for next_point in self._waypoints[1:]:
            distance += self._geo.compute_distance_in_meters(
                current_point, next_point)

            if self._car_in_move(current_point, next_point):
                # only keep the last two point
                move_points = move_points[:2]
                move_points.extend([current_point, next_point])

            elif len(move_points) != 0:
                # if car had moved before it has stopped
                stop_points = stop_points[:2]
                stop_points.extend([current_point, next_point])

            if (self._car_trip_has_ended(stop_points) or
                    self._last_value_in_list(next_point, last_point)):

                # only add a trip with total distance >= 15 meters
                # the start and end point should not be the same
                if (distance >= self.DISTANCE_SHOULD_BE_IGNORED_METERS):
                    start_point = move_points[0]
                    end_point = move_points[-1]
                    trips.append(Trip(
                        round(distance, 3), start_point, end_point))

                # Starting next trip
                # The last stop point should be the begining of the next trip
                move_points = stop_points[-1:]
                stop_points = []
                distance = 0

            current_point = next_point

        return trips
