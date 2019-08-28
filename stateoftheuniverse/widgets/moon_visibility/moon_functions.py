#!/usr/bin/python3
"""
A function to return moon phase & moon brightness.
"""

import numpy as np
import astroplan
import astropy
from astropy.time import Time
import matplotlib.pyplot as plt
from astropy.coordinates import get_moon, get_sun
import datetime

def get_moon_illumination(time: datetime) -> float:
    """ A function to return the moon illumination

    I'll fill this in later
    """

    astropytime = Time(time)
    try:
        illumination = astroplan.moon.moon_illumination(astropytime)
    except:
        print("Something has gone wrong. Please raise an issue on GitHub")
    return illumination*100

def get_moon_state(time: datetime) -> bool:
    """ A function to return whether the moon is waxing or waning
    """
    astropytime = Time(time)
    moonra = get_moon(time).ra.value
    sunra = get_sun(time).ra.value
    opposite = sunra + 180.
    if opposite > 360.:
        opposite -= 360.

    #Find whether waxing or waning
    if sunra > 180:
        if (moonra > sunra) or (moonra < opposite):
            waxing = True
        else:
            waxing=False

    elif sunra <= 180:
        if (moonra > sunra) & (moonra < opposite):
            waxing = True
        else:
            waxing=False

def get_moon_phase(time: datetime) -> str:
    """ Code to get moon phase"""
    illumination = get_moon_illumination(time)
    waxing = get_moon_illumination(time)

    if  illumination <= 0.1:
        phase = 'New Moon'
    if (illumination > 0.1) & (illumination < 49.9):
        if waxing:
            phase = 'Waxing Crescent'
        if not waxing:
            phase = 'Waning Crescent'
    if (illumination >= 49.9) & (illumination <= 50.1):
        if waxing:
            phase = 'First Quarter'
        if not waxing:
            phase = 'Last Quarter'
    if (illumination > 50.1) & (illumination < 99.9):
        if waxing:
            phase = 'Waxing Gibbous'
        if not waxing:
            phase = 'Waning Gibbous'
    if  illumination >= 99.9:
        phase = 'Full Moon'

    return phase

if __name__ == "__main__":
    time = datetime.datetime.now()
    print('{} %'.format(get_moon_illumination(time)))
    print('Our current phase is: {}'.format(get_moon_phase(time)))
