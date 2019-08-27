#!/usr/bin/python3
"""
A function to return moon phase & moon brightness.
"""

import numpy as np
import astroplan
import astropy
from astropy.time import Time

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

# def get_moon_phase(illumination: float):
#     """ A function to return the phase of the moon based on the illumination?
#     """
