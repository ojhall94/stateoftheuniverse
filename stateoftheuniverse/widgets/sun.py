import ephem


# TODO:
# * output formatting (timezones...) - in a separate file
# * return times in a different format (ISO-8601 ?)
# * it can be done in exactly same way for other ephem objects (Moon and planets) so we could
#   abstract this functionality to a common module
# * maybe use astroplan actually, pyephem is easy to use, but not always easy to install
#   (C library) and has a bit bizarre design


def get_sun_info(dt, lat, lon):
    """
    Get times of sunrise and sunset.

    If the Sun is below the horizon, the next sunrise and sunset are returned.
    If it's above the horizon - previous sunrise and next sunset.
    
    Args:
        dt (datetime.datetime): datetime in UTC
        lan (float): geographical latitude
        lon (float): geographical longitude
    Returns:
        A tuple (sunrise time, sunset time) in UTC
    """
    sun = ephem.Sun()

    observer = ephem.Observer()
    observer.date = str(dt)
    observer.lat = str(lat)
    observer.lon = str(lon)

    rising = observer.next_rising(sun)
    setting = observer.next_setting(sun)
    if setting < rising:
        rising = observer.previous_rising()

    return (str(rising), str(setting))
