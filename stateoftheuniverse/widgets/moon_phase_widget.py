from astropy.utils.exceptions import AstropyDeprecationWarning
import warnings

warnings.filterwarnings('ignore', category=AstropyDeprecationWarning)

import astroplan
from astropy.time import Time
from astropy.coordinates import get_moon, get_sun
import datetime as dt
from typing import Optional

from stateoftheuniverse.widgets.prototypes import WidgetPrototype
from stateoftheuniverse.widgets.utils import stringdecorator


class MoonPhaseWidget(WidgetPrototype):
    """
    A widget that calculates the illumination of the moon given the position
    of the moon and the sun on the sky, and calculates the phase of the moon
    given the RA of the moon and the sun.

    Args:
        longitude: the longitude of the user
        latitude: the latitude of the user
        datetime: a datetime.datetime object in UTC
    """

    def __init__(self,
                 longitude: Optional[float] = None,
                 latitude: Optional[float] = None,
                 datetime: Optional[dt.datetime] = None):

        if datetime is None:
            self.datetime = dt.datetime.now()
        else:
            self.datetime = datetime

        super().__init__(longitude=longitude,
                         latitude=latitude,
                         datetime=datetime)

        self.name = 'MOON PHASE INFORMATION'
        self.dict_name = 'moon_phase'

    def get_data(self):
        """
        Call the functions for illumination and moon phase. If these functions
        fail for whatever reason, a boolean variable is stored as false. The
        illumination and phase are stored as properties.
        """

        try:
            self.illumination = self.get_moon_illumination()
            self.phase = self.get_moon_phase()
            self.access_data = True
            return [self.illumination, self.phase]
        except:
            self.access_data = False
            return None

    def get_moon_illumination(self) -> float:
        """
        Calculates the illumination of the moon based on the positions of the
        moon and the sun on the sky.

        Returns:
            A float percentage value between 0 and 100.
        """

        astropytime = Time(self.datetime)
        illumination = astroplan.moon.moon_illumination(astropytime)
        return illumination * 100.

    def get_moon_state(self) -> bool:
        """
        Finds whether the moon is currently waxing or waning based on the
        difference in RA between the moon and the sun on the sky.

        Returns:
            A bool which is true if the moon is waxing, and false if it is
            waning.
        """
        astropytime = Time(self.datetime)
        moonra = get_moon(astropytime).ra.value
        sunra = get_sun(astropytime).ra.value
        opposite = (sunra + 180) % 360

        if sunra > 180:
            waxing = (moonra > sunra) or (moonra < opposite)
        elif sunra <= 180:
            waxing = (moonra > sunra) and (moonra < opposite)

        return waxing

    def get_moon_phase(self) -> str:
        """
        Finds the current phase of the moon depending on the current moon
        illumination, and whether the moon is waxing or waning.

        Returns:
            A string describing the current phase of the moon.
        """
        waxing = self.get_moon_state()

        if self.illumination <= 0.1:
            phase = 'New Moon'
        elif 0.1 < self.illumination < 49.9:
            phase = 'Waxing Crescent' if waxing else 'Waning Crescent'
        elif 49.9 <= self.illumination <= 50.1:
            phase = 'First Quarter' if waxing else 'Last Quarter'
        elif 50.1 < self.illumination < 99.9:
            phase = 'Waxing Gibbous' if waxing else 'Waning Gibbous'
        else:
            phase = 'Full Moon'

        return phase

    @stringdecorator
    def get_string(self) -> str:
        """
        Returns the string representation of the calculated properties.

        Returns: A string with a header describing the calculated illumination
        and moon phase.
        """

        string = ''
        if self.access_data:
            string += (f'The current Moon illumination is: {self.illumination:.2f} %\n')
            string += (f'Our current moon phase is: {self.phase}\n')

        else:
            string += 'No data available.\n'
            string += 'Did you perhaps forget to call ' \
                      'get_data() first or have a problem with your\n' \
                      'internet connection?\n'

        return string


if __name__ == "__main__":
    time = dt.datetime.now()
    widget = MoonPhaseWidget(time)
    widget.get_data()
    print(widget.get_string())
