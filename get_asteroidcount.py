from astroquery.mpc import MPC

def get_NEA(hazard: bool = True,
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

    Some arbitrary change.
    """

    asteroid_count = dict()

    # Get all potentially hazardous asteroids from MPC
    PHA = len(MPC.query_objects('asteroid', pha=1))
    asteroid_count['hazard'] = PHA

    # Get all non-potentially hazardous asteroids greater than 1 km wide from MPC
    NEA_1km = len(MPC.query_objects('asteroid', pha=0, km_neo=1))
    asteroid_count['large'] = NEA_1km

# Get non-potentially hazardous asteroids smaller than 1 km from MPC
    neos = [MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=orbtype) for orbtype in range(10)]
    NEA_count = sum(len(neo) for neo in neos)
    asteroid_count['total'] = NEA_count

    print("We have discovered", asteroid_count['total'], "asteroids.")

    if large:
        print("Of those, there are", asteroid_count['large'], "near-Earth asteroids larger than 1 km wide.")

    if hazard:
        print("Currently, there are", asteroid_count['hazard'], "near-Earth asteroids that are classified as potentially hazardous.")
