import argparse
from datetime import datetime

from stateoftheuniverse.widgets import (
    EphemBodies,
    MoonPhaseWidget,
    ConstellationsWidget,
    ExoplanetCount,
    AsteroidCount,
    AstronomerBirthdays
)


def main():
    parser = argparse.ArgumentParser(description='Input lat and lon')
    # default to Cambridge
    parser.add_argument('lat', type=float, default=52.2)
    parser.add_argument('lon', type=float, default=0.11667)
    args = parser.parse_args()

    dt = datetime.utcnow()

    print("STATE OF THE UNIVERSE\n")
    for widget_class in [
        EphemBodies,
        MoonPhaseWidget,
        ConstellationsWidget,
        ExoplanetCount,
        AsteroidCount,
        AstronomerBirthdays
    ]:
        widget = widget_class(args.lon, args.lat, dt)
        widget.get_data()
        print(widget.get_string())


if __name__ == '__main__':
    main()
