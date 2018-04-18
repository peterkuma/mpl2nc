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

## Variables

- **ad_data_bad_flag**, A/D data bad flag – *0: A/D data good, 1: A/D data probably out of sync. Energy monitor collection is not exactly aligned with MCS shots.*
- **azimuth_angle**, azimuth angle (degrees) – *Azimuth angle of scanner.*
- **background_average**, background average – *Background Average for Channel #1.*
- **background_average_2**, background average (channel 2) – *Background Average for Channel #2.*
- **background_stddev**, background standard deviation – *Background Standard Deviation for channel #1.*
- **background_stddev_2**, background standard deviation (channel 2) – *Background Standard Deviation for Channel #2.*
- **bin_time**, bin time (s) – *Bin width (100, 200, or 500 nanoseconds).*
- **channel_1**, channel #1 data (count us-1) – *For MPL systems without POL-FS option, the return signal array is stored here. For MPL systems with the POL-FS option, the cross-polarized return signal array is stored here.*
- **channel_2**, channel #2 data (count us-1) – *Used only with POL-FS option. The co-polarized return signal array is stored here.*
- **compass_degrees**, compass degrees (degrees) – *Compass degrees (currently unused).*
- **data_file_version**, data file version – *Version of the file format.*
- **elevation_angle**, elevation angle (degrees) – *Elevation angle of scanner.*
- **energy_monitor**, energy monitor – *Mean of the Energy Monitor readings * 1000.*
- **first_background_bin**, first background bin – *Used primarily for MiniMPL (will always be 0 for normal MPL as background is collected pre-trigger).*
- **first_data_bin**, first data bin – *Bin # of the first return data.*
- **gps_altitude**, GPS altitude (m) – *GPS altitude (optional).*
- **gps_latitude**, GPS latitude (degrees north) – *GPS latitude (optional).*
- **gps_longitude**, GPS longitude (degrees east) – *GPS longitude (optional).*
- **mcs_mode**, MCS mode – *MCS mode register.*
- **num_background_bins**, number of background bins (count) – *Number of background bins following First Background Bin.*
- **number_channels**, number of channels (count) – *MCS Channels collected. Either 1 or 2.*
- **number_data_bins**, number of data bins (count) – *Number of data bins (not background) following First Data Bin.*
- **polarization_voltage_0**, polarization voltage 0 – *Not used.*
- **polarization_voltage_1**, polarization voltage 1 – *Not used.*
- **range_calibration**, range calibration (m) – *Default is 0; will indicate range calibration offset measured for particular unit.*
- **scan_scenario_flags**, scan scenario flags – *0: No scan scenario used, 1: Scan scenario used].*
- **shots_sum**, shots sum (count) – *Number of laser shots collected.*
- **sync_pulses_seen_per_second**, sync pulses seen per second (count s-1) – *MiniMPL Only; indicates average number of laser pulses seen to validate if laser is operating correctly.*
- **system_type**, system type – *0: Normal MPL, 1: MiniMPL.*
- **temp_0**, A/D #0 mean – *Mean of the A/D #0 readings * 100.*
- **temp_1**, A/D #1 mean – *Mean of the A/D #1 readings * 100.*
- **temp_2**, A/D #2 mean – *Mean of the A/D #2 readings * 100.*
- **temp_3**, A/D #3 mean – *Mean of the A/D #3 readings * 100.*
- **temp_4**, A/D #4 mean – *Mean of the A/D #4 readings * 100.*
- **time**, time (seconds since 1970-01-01 00:00:00) – *Record collection time.*
- **time_utc**, UTC time (ISO 8601) – *Record collection time (UTC).*
- **trigger_frequency**, trigger frequency (Hz) – *Laser fire rate (usually 2500).*
- **unit**, unit – *Unique number for each data system.*
- **version**, version – *Software version of the EXE that created this file. If the SigmaMPL.exe version is 3.00 then this value would be 300.*
- **ws_barometric_pressure**, barometric pressure (hPa) – *Weather station barometric pressure.*
- **ws_dewpoint**, dewpoint temperature (degree C) – *Weather station dewpoint.*
- **ws_inside_humidity**, inside humidity (percent) – *Weather station inside humidity.*
- **ws_inside_temp**, inside temperature (degree C) – *Weather station inside temperature.*
- **ws_outside_humidity**, outside humidity (percent) – *Weather station outside humidity.*
- **ws_outside_temp**, outside temperature (degree C) – *Weather station outside temperature.*
- **ws_rain_rate**, rain rate (mm h-1) – *Weather station rain rate.*
- **ws_used**, weather station used – *0: Weather station not used, 1: Weather station used.*
- **ws_wind_direction**, wind direction (degree) – *Weather station wind direction.*
- **ws_wind_speed**, wind speed (km h-1) – *Weather station wind speed.*

## Attributes

- **created** – UTC time in ISO 8601 format when the file was created.
- **software** – Software identification (`mpl2nc (https://github.com/peterkuma/mpl2nc)`).
- **version** – mpl2nc version.

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

For support or reporting bugs contact Peter Kuma <<peter.kuma@fastmail.com>>.
