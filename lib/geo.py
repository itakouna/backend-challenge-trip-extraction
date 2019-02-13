import abc
from geopy.distance import vincenty
from pyproj import Geod


class GeoLibrary(metaclass=abc.ABCMeta):
    """
    Define Geo library interface that will be used by Client.
    """

    def __init__(self, geo_library):
        self._geo = geo_library

    @abc.abstractmethod
    def compute_distance_in_meters(self, origin, destination):
        pass


class GeoAdapter(GeoLibrary):
    """
    Adapt the interface of Geo library to the Target interface.
    """

    def compute_distance_in_meters(self, origin, destination):
        return self._geo.compute_distance_in_meters(
            origin, destination)


class GeopyLibrary:
    """
    Define an interface using Geopy library functions.
    """

    def compute_distance_in_meters(self, origin, destination):

        return vincenty((origin.lat, origin.lng),
                        (destination.lat, destination.lng)).meters


class PyprojLibrary:
    """
    Define an interface using Pyproj library functions.
    """

    def compute_distance_in_meters(self, origin, destination):
        geod = Geod(ellps='WGS84')
        _, _, distance = geod.inv(
            origin.lng, origin.lat, destination.lng, destination.lat)
        return distance
