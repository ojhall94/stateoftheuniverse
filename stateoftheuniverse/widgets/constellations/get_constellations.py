import warnings
warnings.filterwarnings("ignore")
from astropy import units as u
from astroplan import Observer
from astropy.coordinates import SkyCoord, AltAz, get_constellation, EarthLocation
from astropy.time import Time
import numpy as np


class ConstellationsWidget():
	def __init__(self, lon=52.2053, lat=0.1218, height=5000, time='2019-08-28'):
		self.lon = lon
		self.lat = lat
		self.height = height

		self.location = self.update_location(self.lon, self.lat, self.height) 
		
		self.time = Time(time + ' 00:00:00')
		
		self.alt,self.az = np.meshgrid(np.arange(5,85,5),np.arange(5,355,5))
		self.alt = self.alt.ravel()
		self.az = self.az.ravel()
	
		self.dome = SkyCoord(az=self.az*u.degree,
				      alt=self.alt*u.degree, 
				      frame=AltAz(obstime=self.time, location=self.location))
		
	def get_data(self):
		self.constellations = list(set(get_constellation(self.dome)))
		return self.constellations

	def update_location(self,lon,lat,height):
		 return EarthLocation.from_geodetic(lon = lon*u.degree, lat= lat*u.degree, height=height*u.meter)

	def get_string(self):
		data = self.get_data()
		data.sort()

		return "Tonight's Constellations are:\n\t" + '\n\t'.join(data)
	
	def check_const(self,const_check):
		if type(const_check) == str:
			if const_check.lower() in [constellation.lower() for constellation in self.constellations]:
				return True
		elif type(const_check) == list:
			bools = []
			for const in const_check:
				if const.lower() in [constellation.lower() for constellation in self.constellations]:
					bools.append(True)
				else:
					bools.append(False)
		else:
			print("Function takes string or list of stings")
			return False
