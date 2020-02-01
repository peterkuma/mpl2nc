#!/usr/bin/env python2.7

from setuptools import setup, find_packages

setup(
    name='mpl2nc',
    version='1.3.2',
    description='Convert Sigma Space Micro Pulse Lidar (MPL) data files to NetCDF',
    author='Peter Kuma',
    author_email='peter.kuma@fastmail.com',
    license='MIT',
    scripts=['mpl2nc'],
    data_files=[('share/man/man1', ['mpl2nc.1'])],
    install_requires=['netCDF4>=1.2.9'],
    keywords=['sigmaspace', 'mpl', 'lidar', 'netcdf'],
    url='https://github.com/peterkuma/mpl2nc',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ]
)
