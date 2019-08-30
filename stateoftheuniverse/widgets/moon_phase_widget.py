
import astroplan
import astropy
from astropy.time import Time
from astropy.coordinates import get_moon, get_sun
import datetime
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

from stateoftheuniverse.widgets.prototypes import WidgetPrototype

class MoonPhaseWidget(WidgetPrototype):

    def __init__(self,
                longitude: Optional[float] = None,
                latitude: Optional[float] = None,
                datetime: Optional[datetime.datetime] = None):
        super().__init__(longitude=longitude,
                         latitude=latitude,
                         datetime=datetime)

    def get_data(self):
        """Fill in docstring"""

        try:
            self.illumination = self.get_moon_illumination()
            self.phase = self.get_moon_phase()
            self.access_data = True
        except:
            self.access_data = False

    def get_moon_illumination(self) -> float:
        """ A function to return the moon illumination
        Test
        I'll fill this in later
        """

        astropytime = Time(self.datetime)
        illumination = astroplan.moon.moon_illumination(astropytime)
        return illumination*100.

    def get_moon_state(self) -> bool:
        """ A function to return whether the moon is waxing or waning
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
        """ Code to get moon phase"""
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

    def get_string(self) -> str:
        string = ''
        string += '\n' + 80 * '-' + '\n'
        string += 'MOON PHASE INFORMATION'.center(80) + '\n'
        string += 80 * '-' + '\n\n'

        if self.access_data:
            string += (f'The current Moon illumination is: {self.illumination:.2f} %\n')
            string += (f'Our current moon phase is: {self.phase}\n\n')

        else:
            string += 'No data available.\n'
            string += 'Did you perhaps forget to call ' \
                      'get_data() first or have a problem with your\n' \
                      'internet connection?\n\n'

        string += 80 * '-' + '\n'
        return string


if __name__ == "__main__":
    time = datetime.datetime.now()
    widget = MoonPhaseWidget(time)
    widget.get_data()
    print(widget.get_string())
