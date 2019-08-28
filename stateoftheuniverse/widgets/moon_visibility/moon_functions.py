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

def get_moon_illumination(time: datetime):
    """ A function to return the moon illumination

    I'll fill this in later
    """

    astropytime = Time(time)
    try:
        illumination = astroplan.moon.moon_illumination(astropytime)
    except:
        print("Something has gone wrong. Please raise an issue on GitHub")
    return illumination

def get_moon_phase(illumination: float):
    """ A function to return the phase of the moon based on the illumination?
    """

if __name__ == "__main__":
    i = []
    ras = []
    rasuns = []
    state = [] #0 waxing 1 waning
    for  d in range(30):
        date = datetime.datetime(2019, 1, d+1)
        time = Time(date)
        moon = get_moon(time)
        sun = get_sun(time)
        ras.append(moon.ra.value)
        rasuns.append(sun.ra.value)

        ra = moon.ra.value
        rasun = sun.ra.value
        if ra > rasun:
            state.append(0)
        elif (ra < rasun-180.):
            state.append(0)
        elif (ra > rasun-180) & (ra < rasun):
            state.append(1)
        elif (ra == rasun):
            state.append(2)
        elif (ra == rasun-180.):
            state.append(3)


    plt.scatter(range(30), ras, c=state)
    plt.axhline(sun.ra.value)
    plt.axhline(sun.ra.value-180.)
    plt.show()
