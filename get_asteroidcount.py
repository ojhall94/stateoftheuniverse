def get_NEA_count(by_method: bool = True,
                        by_class: bool = True) -> dict:
    """
    Get the current total number of confirmed exoplanets from the NASA
    Exoplanet Archive. Additionally, also get the number of exoplanets
    grouped by detection method or by planet class (if desired).
    Args:
        by_method: Whether or not to also return the exoplanet count
            grouped by detection method.
        by_class: Whether or not to also return the exoplanet count
            grouped by (approximate) planet class.
    Returns:
        A dictionary with keys `{"total", "by_method", "by_class"}`
        which holds the respective count of exoplanets.
    """

    # Get all potentially hazardous asteroids from MPC
    PHA = MPC.query_objects('asteroid', pha=1)

    # Get all non-potentially hazardous asteroids greater than 1 km wide from MPC
    NEA_1km = MPC.query_objects('asteroid', pha=0, km_neo=1)

    # Get non-potentially hazardous asteroids smaller than 1 km from MPC
    # (do it in stages since there is a limit to the number of objects that
    # query_objects can call)
    neo0 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=0)
    neo1 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=1)
    neo2 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=2)
    neo3 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=3)
    neo4 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=4)
    neo5 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=5)
    neo6 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=6)
    neo7 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=7)
    neo8 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=8)
    neo9 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=9)
    neo10 = MPC.query_objects('asteroid', pha=0, km_neo=0, neo=1, orbit_type=10)
    NEA_count = len(neo0)+len(neo1)+len(neo2)+len(neo3)+len(neo4)+len(neo5)+len(neo6)+len(neo7)+len(neo8)+len(neo9)+len(neo10)

    total_NEA_count = PHA + NEA_1km + NEA_count

    return total_NEA_count
