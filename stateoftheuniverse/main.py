from datetime import datetime

from widgets import (
    EphemBodies,
    MoonPhaseWidget,
    ConstellationsWidget,
    ExoplanetCount,
    AsteroidCount,
    AstronomerBirthdays
)


def main():
    lat = 52.2
    lon = 0.11667
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
        widget = widget_class(lon, lat, dt)
        widget.get_data()
        print(widget.get_string())


if __name__ == '__main__':
    main()
