from datetime import datetime

import pytest

from stateoftheuniverse.widgets.constellations import ConstellationsWidget

@pytest.mark.parametrize('dt, lat, lon', [
    # Cambridge, before sunrise
    (datetime(2019, 8, 30, 4, 0), 52.2, 0.11667),
    # Cambridge, after sunrise
    (datetime(2019, 8, 30, 16, 0), 30.2, 0.11667),
])

def test_constellations_info(dt, lat, lon): 
	widget = ConstellationsWidget(longitude=lon, latitude=lat, datetime=dt)
	widget1 = ConstellationsWidget(longitude=lon, latitude=lat)
	widget.get_data()
	widget1.get_data()
	assert type(widget.get_string()) == str
	assert type(widget.check_const(widget.constellations)) == list
	assert type(widget.check_const("Ursa Major")) == str
	assert type(widget1.get_string()) == str
	assert type(widget1.check_const(widget.constellations)) == list
	assert type(widget1.check_const("Ursa Major")) == str
