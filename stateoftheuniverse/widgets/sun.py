import ephem


def get_sun_info(dt, lat, lon):
    """
    Get times of sunrise and sunset.

    If the Sun is below the horizon, the next sunrise and sunset are returned.
    If it's above the horizon - previous sunrise and next sunset.
    
    Args:
        dt (datetime.datetime): datetime in UTC
        lat (float): geographical latitude, number between -90 and 90
        lon (float): geographical longitude, number between -180 and 180
    Returns:
        A tuple of two datetime.datetime objects (sunrise, sunset) in UTC
    """
    sun = ephem.Sun()

    observer = ephem.Observer()
    observer.date = str(dt)
    # lat and lon must be converted to strings to make pyephem recognize them
    # as degrees, not radians
    observer.lat = str(lat)
    observer.lon = str(lon)

    rising = observer.next_rising(sun)
    setting = observer.next_setting(sun)
    if setting < rising:
        rising = observer.previous_rising(sun)

    return (rising.datetime(), setting.datetime())
