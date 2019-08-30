from datetime import datetime as dt
import pytest
import numpy as np
from stateoftheuniverse.widgets.moon_phase_widget import MoonPhaseWidget

TIME = dt(2019, 8, 30, 1, 1, 1, 1)

def test_widget_properties():
    """Assert the widget properties are as expected"""
    widget = MoonPhaseWidget(datetime = TIME)
    assert widget.longitude is None
    assert widget.latitude is None
    assert widget.datetime == TIME
    assert widget.name == 'MOON PHASE INFORMATION'

def test_get_data():
    """Assert the widget returns expected data"""
    widget = MoonPhaseWidget(datetime = TIME)
    widget.get_data()

    assert np.isclose(widget.illumination, 0.35, atol = 0.01)
    assert widget.phase == 'Waning Crescent'
