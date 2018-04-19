#!/usr/bin/env python2.7

from setuptools import setup, find_packages

setup(
    name='mpl2nc',
    version='1.1.1',
    description='Convert Sigma Space Micro Pulse Lidar (MPL) data files to NetCDF',
    author='Peter Kuma',
    author_email='peter.kuma@fastmail.com',
    license='MIT',
    scripts=['mpl2nc'],
    install_requires=['netCDF4>=1.2.9'],
    keywords=['sigmaspace', 'mpl', 'lidar', 'netcdf'],
    url='https://github.com/peterkuma/mpl2nc',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ]
)
