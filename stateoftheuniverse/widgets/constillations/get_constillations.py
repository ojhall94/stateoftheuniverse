from astropy import units as u
from astroplan import Observer, FixedTarget
from astropy.coordinates import SkyCoord, AltAz, Angle, get_constellation
from astropy.time import Time
import numpy as np

subaru = Observer.at_site('subaru')

altair = FixedTarget.from_name('Altair')
vega = FixedTarget.from_name('Vega')

time = Time('2019-08-27 12:00:00')

alt = Angle(np.arange(0,90,5), unit=u.deg)
az = Angle(np.arange(0,395,5), unit=u.deg)

#altaz = AltAz(az=az[0], alt=alt[0], location=subaru.location)
altaz = SkyCoord(az=az[1]*u.degree, alt=alt[1]*u.degree, frame='altaz') 
print(subaru.location)
print(type(subaru))
print(altaz)
print(get_constellation(altaz))
