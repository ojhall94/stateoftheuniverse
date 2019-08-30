from astroquery.mpc import MPC
from prototypes import WidgetPrototype

class AsteroidWidget(WidgetPrototype):

    def __init__(self,
                longitude,
                latitude,
                datetime):

        super().__init__(longitude=longitude,
                         latitude=latitude,
                         datetime=datetime)

    def get_data(self,
                hazard: bool = True,
                large: bool = True) -> dict:

        """
        Get the current total number of near-Earth asteroids from the IAU
        Minor Planet Center. Additionally, get the number of asteroids that
        identified as potentially hazardous and larger than 1 km.

        Args:
           hazard: Returning the number of potentially hazardous
               near-Earth asteroids.
           large: Returning the number of near-Earth asteroids that
               are larger than 1 km wide.
        Returns:
            A dictionary with keys `{"hazard", "large", "total"}`
            which holds the respective count of asteroids.
        """

        asteroid_count = dict()

        try:
            # Get all potentially hazardous asteroids from MPC
            pha = len(MPC.query_objects('asteroid', pha=1))
            asteroid_count['hazard'] = pha

            # Get all non-potentially hazardous asteroids greater than 1 km wide from MPC
            nea_1km = len(MPC.query_objects('asteroid', pha=0, km_neo=1))
            asteroid_count['large'] = nea_1km

            # Get non-potentially hazardous asteroids smaller than 1 km from MPC
            # Query by category of asteroid (main belt, Apollos, etc.) due to limits on how many objects query_objects can return at once
            neos = [MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=orbtype) for orbtype in range(11)]
            nea_count = sum(len(neo) for neo in neos)

            # Add all categories of asteroids together for total
            asteroid_count['total'] = nea_count + pha + nea_1km

            # Now that we have retrieved the data, store it
            self.data = asteroid_count

            self.access_data = True

        except:
            self.access_data = False

#    @stringdecorator
    def get_string(self):

        """
        Return string representation of counts of near-Earth
        asteroids that we currently know of from the IAU
        Minor Planet Center.

        Returns:
            A string with a header that gives the number of
            known near-Earth asteroids, as well as the number
            potentially hazardous asteroids and asteroids larger
            than 1 km (if specified by user).
        """

        string = ''

        if self.access_data == False:
            string = 'Error: Cannot retrieve from the IAU Minor Planet Center.\n'\
            'Check your Internet connection and minorplanetcenter.net. '\
            'If both are functional, please raise an issue on Github.'

        else:
            string += f'We have discovered {self.data["total"]} asteroids.'

            if large in self.data.keys():
                string += '\nOf those, there are {self.data["large"]} '\
                'near-Earth asteroids larger than 1 km wide.'

            if hazard in self.data.keys():
                string += '\nCurrently, there are {self.data["hazard"]} '\
                'near-Earth asteroids that are classified as potentially '\
                'hazardous.'

        return string
