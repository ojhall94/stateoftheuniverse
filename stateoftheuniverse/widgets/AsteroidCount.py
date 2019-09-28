"""
Get the current number of asteroids we have discovered.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
from astropy.utils.exceptions import AstropyDeprecationWarning
import warnings

warnings.filterwarnings('ignore', category=AstropyDeprecationWarning)

from astroquery.mpc import MPCClass
from datetime import datetime as dt
from requests.exceptions import ConnectionError
from stateoftheuniverse.widgets.prototypes import WidgetPrototype
from stateoftheuniverse.widgets.utils import stringdecorator
from typing import Optional


# -----------------------------------------------------------------------------
# AUXILIARY METHOD DEFINITIONS
# -----------------------------------------------------------------------------

def nullcontext():
    """
    A custom function that serves as a no-op context manager, which can
    be used with Python version <= 3.6, where contextlib.nullcontext is
    not available.
    Returns:
        A dummy memoryview that serves as a no-op context manager.
    """
    return memoryview(b'')


class SuspendCache:
    """
    A context manager that suspends caching. This code is a direct copy
    from astropy.query, from where it cannot "officially" be imported,
    because it is not exposed through that module's __all__ list.
    """

    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        self.obj._cache_active = False

    def __exit__(self, exc_type, exc_value, traceback):
        self.obj._cache_active = True
        return False


# -----------------------------------------------------------------------------
# CLASS DEFINITIONS
# -----------------------------------------------------------------------------

class AsteroidCount(WidgetPrototype):

    def __init__(self,
                 longitude: Optional[float] = None,
                 latitude: Optional[float] = None,
                 datetime: Optional[dt] = None):

        super().__init__(longitude=longitude,
                         latitude=latitude,
                         datetime=datetime)

        self.name = 'NEAR-EARTH ASTEROIDS'

    def get_data(self,
                 hazard: bool = True,
                 large: bool = True,
                 cache: bool = False):
        """
        Get the current total number of near-Earth asteroids from the
        IAU Minor Planet Center. Additionally, get the number of
        asteroids that have been identified as potentially hazardous
        and larger than 1 km.
        Args:
            hazard: Whether or not to return the number of potentially
                hazardous near-Earth asteroids.
            large: Whether or not to return the number of near-Earth
                asteroids that are larger than 1 km in width.
            cache: Whether or not to cache results or use cached
                results.
        Returns:
            A dictionary with keys `{"hazard", "large", "total"}`
            which holds the respective count of asteroids.
        """

        # Explicitly construct an instance of MPCClass to avoid violating
        # the PEP 8 violating that would result from importing the instance
        # that is automatically created in astroquery.mpc. We need this
        # instance for the cache context manager (see below).
        mpc = MPCClass()

        # Define a helper function for querying data from the MPC:
        # By default, astroquery does not provide a way to choose whether
        # or not to use caching with the MPCClass.query_objects() method.
        # Instead, it simply defaults to always using cached results.
        # We mitigate this issue by defining our own function for sending
        # queries to the MPC, which wraps the MPCClass instance into a
        # suspend_cache context manager in case we want to disable the cache.
        def query_objects(*args, **kwargs):
            context_manager = nullcontext() if cache else SuspendCache(mpc)
            with context_manager:
                return mpc.query_objects(*args, **kwargs)

        asteroid_count = dict()

        # Send queries to the MPC. In case we do not have internet access (and
        # thus get an ConnectionError), we do not write anything to self.data.
        try:

            # Get all potentially hazardous asteroids (PHA) from MPC
            if hazard:
                pha = len(query_objects('asteroid', pha=1))
                asteroid_count['hazard'] = pha
            else:
                pha = 0

            # Get all non-potentially hazardous near-Earth asteroids (NEA)
            # greater than 1 km wide from the MPC
            if large:
                nea_1km = len(query_objects('asteroid', pha=0, km_neo=1))
                asteroid_count['large'] = nea_1km
            else:
                nea_1km = 0

            # Get non-potentially hazardous asteroids smaller than 1 km
            # from MPC
            # Query by category of asteroid (main belt, Apollos, etc.) due to
            # limits on how many objects query_objects can return at once
            nea_count = sum(len(query_objects('asteroid', pha=0, km_neo=0,
                                              neo=1, orbit_type=orbtype))
                            for orbtype in range(11))

            # Add all categories of asteroids together for total
            asteroid_count['total'] = nea_count + pha + nea_1km

            # Now that we have retrieved the data, store it
            self.data = asteroid_count

        # If we cannot establish a connection to the MPC server,
        # we do not write any results to self.data
        except ConnectionError:
            return

    @stringdecorator
    def get_string(self):
        """
        Return string representation of counts of near-Earth asteroids
        that we currently know of from the IAU Minor Planet Center.
        Returns:
            A string with a header that gives the number of known
            near-Earth asteroids, as well as the number potentially
            hazardous asteroids and asteroids larger than 1 km
            (if specified by user).
        """

        string = ''

        if self.data is None:
            string = 'Error: Could not retrieve data from the IAU Minor ' \
                     'Planet Center (MPC).\n\n' \
                     'Please check your internet connection and ' \
                     'minorplanetcenter.net.\n' \
                     'If both are functional, please raise an issue on ' \
                     'GitHub.\n'

        else:
            string += f'We have discovered {self.data["total"]} asteroids.\n'

            if 'large' in self.data.keys():
                string += f'Of those, there are {self.data["large"]} ' \
                          'near-Earth asteroids larger than 1 km wide.\n'

            if 'hazard' in self.data.keys():
                string += f'Currently, there are {self.data["hazard"]} ' \
                          'near-Earth asteroids that are classified as\n' \
                          'potentially hazardous.\n'

        return string
