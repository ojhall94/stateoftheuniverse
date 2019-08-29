from astroquery.mpc import MPC

class AsteroidWidget():

    def __init__(self,
               longitude: Optional[float] = None,
               latitude: Optional[float] = None,
               datetime: Optional[dt] = None):

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
            neos = [MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=orbtype) for orbtype in range(10)]
            nea_count = sum(len(neo) for neo in neos)

            # Add all categories of asteroids together for total
            asteroid_count['total'] = nea_count + pha + nea_1km

            # Now that we have retrieved the data, store it
            self.data = asteroid_count

        except:
            access_data = False

    def get_string(self):

        if access_data = False:
            print("Error: Cannot retrieve from the IAU Minor Planet Center.")
            print("Check your Internet connection and minorplanetcenter.net. If both are functional, please raise an issue on Github.")

        else:
            print("We have discovered", asteroid_count['total'], "asteroids.")

            if large:
                print("Of those, there are", asteroid_count['large'], "near-Earth asteroids larger than 1 km wide.")

            if hazard:
                print("Currently, there are", asteroid_count['hazard'], "near-Earth asteroids that are classified as potentially hazardous.")
