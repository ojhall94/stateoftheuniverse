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
from stateoftheuniverse.widgets.prototypes import WidgetPrototype
from stateoftheuniverse.widgets.utils import stringdecorator

#-------------------------
# Function Definitions
#------------------------
class ConstellationsWidget(WidgetPrototype):
	"""
	A widget that collects and holds list of constellations which will 
	be in the sky at the users location at midnight

	Args:
	    longitude: the longitude of the user
	    latitude: the latitude of the user
	    datetime: a datetime.datetime object in UTC
	"""
	def __init__(self,
                     longitude: Optional[float] = None,
                     latitude: Optional[float] = None,
                     datetime: Optional[dt] = None):
		super().__init__(longitude=longitude,
		                 latitude=latitude,
		                 datetime=datetime) 

		self.height = 1500

		self.location = EarthLocation.from_geodetic(lon = self.longitude*u.degree, 
							    lat= self.latitude*u.degree, 
							    height=self.height*u.meter)

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
		Update and store list of tonight's constellations, based on the users 
		location. Uses a matrix of points on the sky to retrieve constellations
		that they are located in.
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

		if self.constellations == None:
			self.get_data()
		if type(const_check) == str:
			if const_check.lower() in [constellation.lower() for constellation in self.constellations]:
				return f"{const_check} will be visible tonight."
			else:
				return f"{const_check} will not be visible tonight."
		elif type(const_check) == list:
			avail_consts = []
			for const in const_check:
				if const.lower() in [constellation.lower() for constellation in self.constellations]:
					avail_consts.append(f"{const} will be visible tonight.")
				else:
					avail_consts.append(f"{const} will not be visible tonight.")
			return avail_consts
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

