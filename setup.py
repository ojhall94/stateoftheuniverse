from setuptools import setup

setup(name='State of the Universe',
      version='0.0',
      description='Generate an overview of the current state of the Universe!',
      url='https://github.com/ojhall94/stateoftheuniverse',
      install_requires=['astropy',
                        'astroquery',
                        'jinja2',
                        'numpy',
                        'python-dateutil',
                        'scipy',
                        'matplotlib',
                        'requests',
                        'SPARQLWrapper'],
      packages=['stateoftheuniverse'],
      zip_safe=False)
