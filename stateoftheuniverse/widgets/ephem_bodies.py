import ephem
import pytz
import timezonefinder

from stateoftheuniverse.widgets.prototypes import WidgetPrototype
from stateoftheuniverse.widgets.utils import stringdecorator

# TIMEZONE = pytz.timezone('Europe/London')

EPHEM_BODIES = [
    ephem.Sun(),
    ephem.Moon(),
    ephem.Mercury(),
    ephem.Venus(),
    ephem.Mars(),
    ephem.Jupiter(),
    ephem.Saturn(),
    # ephem.Uranus(),
    # ephem.Neptune(),
]


class EphemBodies(WidgetPrototype):

    def __init__(
            self,
            longitude: float,
            latitude: float,
            datetime,
    ):
        super().__init__(longitude, latitude, datetime)

        self.name = "Solar System bodies visibility"

        self.observer = ephem.Observer()
        # datetime must be in UTC!!!
        self.observer.date = str(datetime)
        # lat and lon must be converted to strings to make pyephem recognize them
        # as degrees, not radians
        self.observer.lat = str(latitude)
        self.observer.lon = str(longitude)

        tf = timezonefinder.TimezoneFinder()
        tz_str = tf.timezone_at(lng=longitude, lat=latitude)
        self.timezone = pytz.timezone(tz_str)
        self.local_datetime = datetime.astimezone(self.timezone)

    def get_data(self):
        """
        Get times of rising and setting of the given body in UTC.

        If the body is below the horizon, the next rising and setting are returned.
        If it's above the horizon - previous rising and next setting.
        """
        self.data = {}
        for body in EPHEM_BODIES:
            rising = self.observer.next_rising(body)
            setting = self.observer.next_setting(body)
            if setting < rising:
                rising = self.observer.previous_rising(body)

            self.data[body.name] = (rising.datetime(), setting.datetime())

    @stringdecorator
    def get_string(self):
        return (
                f'Data computed for {dt_minutes(self.local_datetime)} in timezone {self.timezone}, '
                f'latitude {self.latitude}, longitude {self.longitude}\n\n' +
                f'\n'.join(
                    self.body_summary(name, v[0], v[1])
                    for name, v in self.data.items()
                )
        )

    def body_summary(self, name, rising, setting):
        # Convert all datetimes from UTC to local timezone
        rising = rising.astimezone(self.timezone)
        setting = setting.astimezone(self.timezone)

        # Body is below the horizon and won't rise today
        if rising.date() > self.local_datetime.date():
            summary = f"{name} doesn't rise today. Will rise on {dt_minutes(rising)}"
        else:
            summary = f"{name} rises on {dt_minutes(rising)} and sets on {dt_minutes(setting)}"

        return summary


def dt_minutes(dt):
    """Format a datetime with precision to minutes."""
    return dt.strftime('%Y-%m-%d %H:%M')


def time_minutes(dt):
    """Format a datetime as time only with precision to minutes."""
    return dt.strftime('%H:%M')
