# mpl2nc

Convert Sigma Space Micro Pulse Lidar (MPL) data files to NetCDF.

mpl2nc is a Python program for converting binary MPL files to NetCDF4. The
converted variables closely follow those in the binary files. See the *Micro
Pulse LiDAR System Software Manual* for description of the original format and
variables. 

The program uses Python 2.7 and can run on any operating system with
Python 2.7 and the netCDF4 Python package installed.

**Note:** The current release is beta – feature-complete but not tested comprehensively yet.

## Usage

```sh
mpl2nc [-h] [-v] <input> <output>
```

Optional arguments:

- **-h** – show help message and exit
- **-v** – show program's version number and exit

Positional arguments: 
- **input** – input file (mpl)
- **output** – output file (NetCDF)

## Install

Install the required software:

- Python 2.7 (recommended Anaconda/Python 2.7 on Windows)
- netCDF4 Python package

netCDF4 can be installed with pip if available in your Python distribution:

```sh
pip install netCDF4
```

To install mpl2nc with pip:

```sh
pip install mpl2nc
````

Optionally, to install from the source distribution:

```sh
python setup.py install
```

## License

This software is distributed under the terms of the MIT License
(see [LICENSE.md](LICENSE.md) in the source distribution).

## Release Notes

Version numbering follows [Semantic Versioning](https://semver.org/).

### 1.1.0 (2018-04-18)

- Added global file attributes.
- Fixed syntax error in the script.

### 1.0.0 (2018-04-18)

- Initial version.

## Contact

For support or reporting bugs contact Peter Kuma <peter.kuma@fastmail.com>.
