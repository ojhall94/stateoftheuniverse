from setuptools import setup

setup(name='stateoftheuniverse',
      version='0.0',
      description='Generate an overview of the current state of the Universe!',
      url='https://github.com/ojhall94/stateoftheuniverse',
      install_requires=['astropy',
                        'astroquery',
                        'python-dateutil',
                        'SPARQLWrapper',
                        'astroplan',
                        'pyephem',
                        'pytz',
                        'timezonefinder'],
      test_requires=['pytest'],
      packages=['stateoftheuniverse', 'stateoftheuniverse.widgets'],
      entry_points={
          'console_scripts': ['stateoftheuniverse = stateoftheuniverse.main:main']
      },
      zip_safe=False)
