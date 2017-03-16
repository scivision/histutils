#!/usr/bin/env python
from setuptools import setup

req= ['pathvalidate','pymap3d','sciencedates',
      'python-dateutil','pytz','nose','numpy','scipy','pandas','h5py','astropy','matplotlib','seaborn']


setup(name='histutils',
      packages=['histutils'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/histutils',
      description='Utilities for reading HiST data, etc.',
      version='0.9.2',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3.6',
      ],
	  install_requires=req,
      extras_require={'tifffile':['tifffile'],
                        'dascutils':['dascutils'],
                        'themisasi':['themisasi']},

	  )

