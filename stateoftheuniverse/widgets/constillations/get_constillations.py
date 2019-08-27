from astroplan import Observer, FixedTarget
from astropy.coordinates import SkyCoord
from astropy.time import Time

subaru = Observer.at_site('subaru')

altair = FixedTarget.from_name('Altair')
vega = FixedTarget.from_name('Vega')

time = Time('2019-08-27 12:00:00')

print(subaru.target_is_up(time,altair))
