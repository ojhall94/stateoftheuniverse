from astropy import units as u
from astroplan import Observer
from astropy.coordinates import SkyCoord, AltAz, get_constellation, EarthLocation
from astropy.time import Time
import numpy as np

#user = Observer.at_site('subaru')
user = EarthLocation.from_geodetic(lon = 52.2053*u.degree, lat= 0.1218*u.degree, height=5000*u.meter)

time = Time('2019-08-28 00:00:00')

alt = np.arange(0,85,5)
az = np.arange(0,355,5)
alt,az = np.meshgrid(alt,az)
alt = alt.ravel()
az = az.ravel()

altaz = SkyCoord(az=az*u.degree,
		 alt=alt*u.degree, 
		 frame=AltAz(obstime=time, location=user))

const = get_constellation(altaz)
print(set(const))
