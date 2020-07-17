#!/usr/bin/env python

from setuptools import setup

setup(
    name='mpl2nc',
    version='1.3.4',
    description='Convert Sigma Space Micro Pulse Lidar (MPL) data files to NetCDF',
    author='Peter Kuma',
    author_email='peter@peterkuma.net',
    license='MIT',
    py_modules=['mpl2nc'],
    entry_points={
        'console_scripts': ['mpl2nc=mpl2nc:main'],
    },
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
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ]
)
