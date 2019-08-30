import argparse
from datetime import datetime

from geopy.geocoders import Nominatim

from stateoftheuniverse.widgets import (
    EphemBodies,
    MoonPhaseWidget,
    ConstellationsWidget,
    ExoplanetCount,
    AsteroidCount,
    AstronomerBirthdays
)


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('lat', type=float)
    # parser.add_argument('lon', type=float)
    # args = parser.parse_args()
    # lat = args.lat
    # lon = args.lon

    parser.add_argument('place', type=str)
    args = parser.parse_args()

    geolocator = Nominatim()
    loc = geolocator.geocode(args.place)
    lat = loc.latitude
    lon = loc.longitude

    dt = datetime.utcnow()

    for widget_class in [
        EphemBodies,
        MoonPhaseWidget,
        ConstellationsWidget,
        ExoplanetCount,
        AsteroidCount,
        AstronomerBirthdays
    ]:
        widget = widget_class(lon, lat, dt)
        widget.get_data()
        print(widget.get_string())


if __name__ == '__main__':
    main()
