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


class WaypointListProcessor(ListProcessor):

    def __init__(self, waypoints):
        self._geo = GeoAdapter(GeopyLibrary())
        super().__init__(waypoints)

    def _car_in_move(self, current_point: Waypoint, next_point: Waypoint) -> bool:
        return (current_point.lat != next_point.lat or
                current_point.lng != next_point.lng)

    def get_trips(self) -> Tuple[Trip]:
        pass
