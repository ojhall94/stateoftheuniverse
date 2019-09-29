import argparse
from datetime import datetime
from flask import Flask, render_template

from geopy.geocoders import Nominatim

from stateoftheuniverse.widgets import (
    EphemBodies,
    MoonPhaseWidget,
    ConstellationsWidget,
    ExoplanetCount,
    #    AsteroidCount,
    AstronomerBirthdays
)


def get_data():
    #    parser = argparse.ArgumentParser()
    # parser.add_argument('lat', type=float)
    # parser.add_argument('lon', type=float)
    # args = parser.parse_args()
    # lat = args.lat
    # lon = args.lon
    #    parser.add_argument('place', type=str)
    #    args = parser.parse_args()

    geolocator = Nominatim()
    loc = geolocator.geocode("knoxville")  # args.place)
    lat = loc.latitude
    lon = loc.longitude

    dt = datetime.utcnow()

    data = {}

    for widget_class in [
        #            EphemBodies,
        MoonPhaseWidget,
        ConstellationsWidget,
        #            ExoplanetCount,
        #            AsteroidCount,
        AstronomerBirthdays
    ]:
        widget = widget_class(lon, lat, dt)
        data[widget.dict_name] = {'name': widget.name, 'data': widget.get_data()}
        print(data)
    return data


app = Flask(__name__)

data=get_data()

@app.route("/")
def home():
    return render_template("base.html", dictionary=data)  # "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
