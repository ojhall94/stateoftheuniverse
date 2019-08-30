"""
Get the current number of exoplanets (grouped by different categories).
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

import astropy.units as u

from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from collections import Counter
from datetime import datetime as dt
from typing import Optional
from urllib.error import URLError

from stateoftheuniverse.widgets.prototypes import WidgetPrototype


# -----------------------------------------------------------------------------
# AUXILIARY FUNCTION DEFINITIONS
# -----------------------------------------------------------------------------

def get_exoplanet_class(mass: u.Quantity,
                        radius: u.Quantity) -> str:
    """
    (Approximately) classify an exoplanet based on its mass and radius.

    The classification scheme used here is based on the table from:
        http://phl.upr.edu/library/notes/
            amassclassificationforbothsolarandextrasolarplanets

    Args:
        mass: The mass of the exoplanet as a astropy.units.Quantity.
        radius: The radius of the exoplanet as a astropy.units.Quantity.

    Returns:
        The approximate planet class, which is one of the following:
            ["Asteroidan", "Mercurian", "Subterran", "Terran",
             "Superterran", "Neptunian", "Jovian", "N/A", "Other"]
    """

    # Convert mass and radius to Earth units and cast to float
    mass = mass.to(u.earthMass).to_value()
    radius = radius.to(u.earthRad).to_value()

    # Classify the planet based on its mass and radius
    if (mass == 0) or (radius == 0):
        return 'N/A'
    elif (0 < mass <= 0.00001) and (0 < radius <= 0.03):
        return 'Asteroidan'
    elif (0.00001 <= mass <= 0.1) and (0.03 <= radius <= 0.7):
        return 'Mercurian'
    elif (0.1 <= mass <= 0.5) and (0.5 <= radius <= 1.2):
        return 'Subterran'
    elif (0.5 <= mass <= 2) and (0.8 <= radius <= 1.9):
        return 'Terran'
    elif (2 <= mass <= 10) and (1.3 <= radius <= 3.3):
        return 'Superterran'
    elif (10 <= mass <= 50) and (2.1 <= radius <= 5.7):
        return 'Neptunian'
    elif (50 <= mass < 5000) and (3.5 <= radius <= 27):
        return 'Jovian'
    else:
        return 'Other'


# -----------------------------------------------------------------------------
# CLASS DEFINITIONS
# -----------------------------------------------------------------------------

class ExoplanetCount(WidgetPrototype):

    def __init__(self,
                 longitude: Optional[float] = None,
                 latitude: Optional[float] = None,
                 datetime: Optional[dt] = None):

        super().__init__(longitude=longitude,
                         latitude=latitude,
                         datetime=datetime)

    def get_data(self,
                 by_method: bool = True,
                 by_class: bool = True,
                 cache: bool = True):
        """
        Get the current total number of confirmed exoplanets from the
        NASA Exoplanet Archive. Additionally, also get the number of
        exoplanets grouped by detection method or by planet class (if
        desired).

        Args:
            by_method: Whether or not to also return the exoplanet count
                grouped by detection method.
            by_class: Whether or not to also return the exoplanet count
                grouped by (approximate) planet class.
            cache: Whether or not to cache results or use cached
                results.

        Returns:
            A dictionary with keys `{"total", "by_method", "by_class"}`
            which holds the respective count of exoplanets.
        """

        # Instantiate the dictionary that will hold the results
        exoplanet_count = dict()

        # Get the confirmed exoplanets form the NASA Exoplanet Archive.
        # In case we do not have internet access (and thus get an URLError),
        # the function ends here already (i.e., self.data will remain None).
        try:
            confirmed_exoplanets = \
                NasaExoplanetArchive.get_confirmed_planets_table(cache=cache)
        except URLError:
            return

        # Get the total count of all confirmed planets
        exoplanet_count['total'] = len(confirmed_exoplanets)
    
        # Get count by detection method
        if by_method:
            exoplanet_count['by_method'] = \
                dict(Counter(list(confirmed_exoplanets['pl_discmethod'])))

        # Get count by planet class (by looping over all confirmed exoplanets
        # and classifying each of them based on its respective mass and radius)
        if by_class:

            # Initialize the sub-dictionary that will hold the counts per class
            exoplanet_count['by_class'] = dict()
        
            # Loop over all confirmed exoplanets and classify them individually
            for i in range(len(confirmed_exoplanets)):

                # Get the mass and radius and cast to a astropy.units.Quantity
                # Note: The NASA Exoplanet Archive usually returns values in
                #       Jupiter units.
                mass = float(
                    str(confirmed_exoplanets[i]['pl_bmassj']).split()[0])
                mass = u.Quantity(mass, u.jupiterMass)
                radius = float(
                    str(confirmed_exoplanets[i]['pl_radj']).split()[0])
                radius = u.Quantity(radius, u.jupiterRad)

                # Classify the exoplanet based on these values
                planet_class = get_exoplanet_class(mass=mass, radius=radius)

                # Increase the count for the planet class
                if planet_class in exoplanet_count['by_class'].keys():
                    exoplanet_count['by_class'][planet_class] += 1
                else:
                    exoplanet_count['by_class'][planet_class] = 1

        # Store away the data retrieved by this method
        self.data = exoplanet_count

    def get_string(self):

        string = ''
        string += '\n' + 80 * '-' + '\n'
        string += 'NUMBER OF CONFIRMED EXOPLANETS'.center(80) + '\n'
        string += 80 * '-' + '\n\n'

        # If data is available, build a string from it
        if self.data is not None:

            # Get the maximum key and value length for aligning the output
            max_key_length = max(max(map(len, self.data['by_method'].keys())),
                                 max(map(len, self.data['by_class'].keys())))
            max_key_length += 3
            max_val_length = max(map(lambda x: len(str(x)),
                                     self.data['by_method'].values()))

            string += f'{"Total number:":<{max_key_length}}' \
                f'{self.data["total"]:>{max_val_length}}\n'

            # Add number for each detection method, sorted descendingly
            string += '\nBy detection method:\n'
            for method, count in sorted(self.data['by_method'].items(),
                                        key=lambda x: x[1], reverse=True):
                method = '  ' + method + ':'
                string += f'{method:<{max_key_length}}' \
                    f'{count:>{max_val_length}}\n'

            # Add number for each planet class, sorted descendingly
            string += '\nBy exoplanet class:\n'
            for planet_class, count in sorted(self.data['by_class'].items(),
                                              key=lambda x: x[1],
                                              reverse=True):
                method = '  ' + planet_class + ':'
                string += f'{method:<{max_key_length}}' \
                    f'{count:>{max_val_length}}\n'

        # Otherwise, return a default message that something went wrong
        else:

            string += 'No data available.\n'
            string += 'Did you perhaps forget to call ' \
                      'get_data() first or have a problem with your\n' \
                      'internet connection?\n'

        string += '\n' + 80 * '-' + '\n'

        return string
