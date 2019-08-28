from astropy import units as u
from astroplan import Observer
from astropy.coordinates import SkyCoord, AltAz, get_constellation, EarthLocation
from astropy.time import Time
import numpy as np


class ConstellationsWidget():
	def __init(self, lon=52.2053, lat=0.1218, height=5000, time='2019-08-28'):
		self.lon = lon
		self.lat = lat
		self.height = height

		self.location = update_location(self.lon, self.lat, self.height) 
		
		self.time = Time(time + ' 00:00:00')
		
		self.alt,self.az = np.meshgrid(np.arange(0,355,5),np.arange(0,85,5))
		self.alt = alt.ravel()
		self.az = az.ravel()
			
		self.dome = SkyCoord(az=az*u.degree,
				      alt=alt*u.degree, 
				      frame=AltAz(obstime=time, location=self.location))
		
	def get_consts(self.altaz):
		return set(get_constellation(self.dome))

	def update_location(lon,lat, height):
		self.location = EarthLocation.from_geodetic(lon = lon*u.degree, lat= lat*u.degree, height=height*u.meter)
