"""
Prototype class for widgets.
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

from abc import abstractmethod, ABC
from datetime import datetime as dt

from typing import Optional


# -----------------------------------------------------------------------------
# CLASS DEFINITIONS
# -----------------------------------------------------------------------------

class WidgetPrototype(ABC):

    @abstractmethod
    def __init__(self,
                 longitude: Optional[float] = None,
                 latitude: Optional[float] = None,
                 datetime: Optional[dt] = None):

        self.longitude = longitude
        self.latitude = latitude

        if datetime is None:
            self.datetime = dt.now()

        self.data = None

    @abstractmethod
    def get_data(self):
        raise NotImplementedError

    @abstractmethod
    def get_string(self):
        raise NotImplementedError
