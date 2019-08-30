"""
Get a list of constellations that will be visible from a location on the earth as a given time.
"""
#-------------------------
#Imports
#------------------------
import warnings
warnings.filterwarnings("ignore")
from datetime import date as dt
from astropy import units as u
from astroplan import Observer
from astropy.coordinates import SkyCoord, AltAz, get_constellation, EarthLocation
from astropy.time import Time
import numpy as np

#-------------------------
# Function Definitions
#------------------------
class ConstellationsWidget():
	"""
	
	"""
	def __init__(self, 
		longitude = 52.2053, 
		latitude = 0.1218, 
		height = 15000, 
		time = None):

		self.longitude = longitude
		self.latitude = latitude
		self.height = height

		self.location = EarthLocation.from_geodetic(lon = self.longitude*u.degree, lat= self.latitude*u.degree, height=self.height*u.meter)

		if time == None:
			self.datetime = dt.today()
			self.datetime = str(self.datetime)[:10] + ' 23:00:00'
			self.time = Time(self.datetime)

		elif len(time) > 10:
			self.time = Time(time)

		elif len(time) == 10:
			self.time = Time(time + ' 23:00:00')

		else:
			print("Time must left be of the form YYYY-MM-DD or not passed for tonights sky")
		
		self.alt,self.az = np.meshgrid(np.arange(5,85,5),np.arange(5,355,5))
		self.alt = self.alt.ravel()
		self.az = self.az.ravel()
	
		self.dome = SkyCoord(az=self.az*u.degree,
				      alt=self.alt*u.degree, 
				      frame=AltAz(obstime=self.time, location=self.location))
		self.data = None
		
	def get_data(self):
		"""
		Return list of tonight's constellations.
		"""

		self.constellations = list(set(get_constellation(self.dome)))
		self.constellations.sort()
		return self.constellations

	def update_location(self,longitude,latitude,height):
		"""
		Update location from which constellations should be visible.
		"""
		
		self.longitude = longitude
		self.latitude = latitude
		self.height = height
		self.location = EarthLocation.from_geodetic(lon = self.longitude*u.degree, lat= self.latitude*u.degree, height=self.height*u.meter)

	def get_string(self):
		"""
		Return formatted output string of visible constellations.
		"""
		print(type(self.data))
		if self.data == None:
			self.data = self.get_data()

		return "Tonight's Constellations are:\n\t" + '\n\t'.join(self.data)
	
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
