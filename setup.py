from setuptools import setup

setup(name='State of the Universe',
      version='0.0',
      description='Generate an overview of the current state of the Universe!',
      url='https://github.com/ojhall94/stateoftheuniverse',
      install_requires=['astroquery',
                        'jinja2',
                        'numpy',
                        'scipy',
                        'matplotlib',
                        'requests',
                        'pyephem'],
      packages=['stateoftheuniverse'],
      zip_safe=False)
