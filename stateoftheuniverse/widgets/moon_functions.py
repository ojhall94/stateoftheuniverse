
import astroplan
import astropy
from astropy.time import Time
from astropy.coordinates import get_moon, get_sun
import datetime
import matplotlib.pyplot as plt
import numpy as np

def get_moon_illumination(time: datetime.datetime) -> float:
    """ A function to return the moon illumination
    Test
    I'll fill this in later
    """

    astropytime = Time(time)
    try:
        illumination = astroplan.moon.moon_illumination(astropytime)
    except:
        print("Something has gone wrong. Please raise an issue on GitHub")
    return illumination*100.

def get_moon_state(time: datetime.datetime) -> bool:
    """ A function to return whether the moon is waxing or waning
    """
    astropytime = Time(time)
    moonra = get_moon(time).ra.value
    sunra = get_sun(time).ra.value
    opposite = sunra + 180.
    if opposite > 360.:
        opposite -= 360.

    if sunra > 180:
        waxing = (moonra > sunra) or (moonra < opposite)
    elif sunra <= 180:
        waxing = (moonra > sunra) and (moonra < opposite)

def get_moon_phase(time: datetime.datetime) -> str:
    """ Code to get moon phase"""
    illumination = get_moon_illumination(time)
    waxing = get_moon_state(time)

    if illumination <= 0.1:
        phase = 'New Moon'
    elif 0.1 < illumination < 49.9:
        phase = 'Waxing Crescent' if waxing else 'Waning Crescent'
    elif 49.9 <= illumination <= 50.1:
        phase = 'First Quarter' if waxing else 'Last Quarter'
    elif 50.1 < illumination < 99.9:
        phase = 'Waxing Gibbous' if waxing else 'Waning Gibbous'
    else:
        phase = 'Full Moon'

    return phase

if __name__ == "__main__":
    time = Time(datetime.datetime.now())
    print(f'{get_moon_illumination(time):.2f} %')
    print(f'Our current moon phase is: {get_moon_phase(time)}')
