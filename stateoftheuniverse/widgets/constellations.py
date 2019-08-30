"""
Get a list of constellations that will be visible from a location on the earth as a given time.
"""
#-------------------------
#Imports
#------------------------
from datetime import datetime as dt
from astropy import units as u
from astroplan import Observer
from astropy.coordinates import SkyCoord, AltAz, get_constellation, EarthLocation
from astropy.time import Time
import numpy as np
from typing import Optional
from prototypes import WidgetPrototype
from utils import stringdecorator

#-------------------------
# Function Definitions
#------------------------
class ConstellationsWidget(WidgetPrototype):
	"""
	
	"""
	def __init__(self,
                     longitude: Optional[float] = None,
                     latitude: Optional[float] = None,
                     datetime: Optional[dt] = None):
		super().__init__(longitude=longitude,
		                 latitude=latitude,
		                 datetime=datetime) 

		self.height = 1500

		self.location = EarthLocation.from_geodetic(lon = self.longitude*u.degree, lat= self.latitude*u.degree, height=self.height*u.meter)

		if self.datetime == None:
			self.datetime = dt.now()
			self.datetime = str(self.datetime)[:10] + ' 23:00:00'
			self.time = Time(self.datetime)

		else:
			self.time = Time(self.datetime)
		
		self.alt,self.az = np.meshgrid(np.arange(5,85,5),np.arange(5,355,5))
		self.alt = self.alt.ravel()
		self.az = self.az.ravel()

		self.dome = SkyCoord(az=self.az*u.degree,
				     alt=self.alt*u.degree, 
				     frame=AltAz(obstime=self.time, location=self.location))
		self.constellations = None
		self.name = "CONSTELLATIONS"
		
	def get_data(self):
		"""
		Update and store list of tonight's constellations.
		"""

		self.constellations = list(set(get_constellation(self.dome)))
		self.constellations.sort()

#	def update_location(self,longitude,latitude,height):
#		"""
#		Update location from which constellations should be visible.
#		"""
#		
#		self.longitude = longitude
#		self.latitude = latitude
#		self.height = height
#		self.location = EarthLocation.from_geodetic(lon = self.longitude*u.degree, lat= self.latitude*u.degree, height=self.height*u.meter)
#		self.dome = SkyCoord(az=self.az*u.degree,
#				     alt=self.alt*u.degree, 
#				     frame=AltAz(obstime=self.time, location=self.location))

	@stringdecorator
	def get_string(self):
		"""
		Return formatted output string of visible constellations.
		"""
		if self.constellations == None:
			self.get_data()

		string =  "Tonight's Constellations are:\n\t" + '\n\t'.join(self.constellations)
		return string 

	def check_const(self,const_check):
		"""
		Return bool or list of bools for if a given constellation will be in visible on data.
		"""
	
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
			if all(bools):
				return True
			return False
		else:
			print("Function takes string or list of stings")
			return False


if __name__ == "__main__":
	const = ConstellationsWidget(longitude=52.2053, latitude=0.1218)

	print(const.get_string())

	for constellation in const.constellations: 
		if not const.check_const(str(constellation)):
			print("Failed to find " + constellation)

	print(const.check_const(const.constellations))

