#!/usr/bin/env python

import sys
import os
import argparse
import logging
import struct
import datetime as dt

import numpy as np
from netCDF4 import Dataset

__version__ = '1.3.3'

C = 299792458 # m.s-1

TYPES = {
    'float32': 'f',
    'float64': 'd',
    'int16': 'h',
    'int32': 'i',
    'uint8': 'B',
    'uint16': 'H',
    'uint32': 'I',
}

TYPE_SIZE = {
    'float32': 4,
    'float64': 8,
    'int16': 2,
    'int32': 4,
    'uint8': 1,
    'uint16': 2,
    'uint32': 4,
}

NC_TYPE = {
    'float32': 'f4',
    'float64': 'f8',
    'int8': 'i1',
    'int16': 'i2',
    'int32': 'i4',
    'S19': 'S19',
    'uint8': 'u1',
    'uint16': 'u2',
    'uint32': 'u4',
    'uint64': 'u8',
}

FILL_VALUE = {
    'float32': -999.0,
    'float64': -999.0,
    'int8': 255,
    'int16': -999,
    'int32': 2147483647,
    'S19': '',
    'uint8': 255,
    'uint16': -999,
    'uint32': 4294939996,
    'uint64': 18446744073709551615,
}

HEADER_MPL = [
    ['unit', 'uint16', 'unit', 'Unique number for each data system.', None, ['profile']],
    ['version', 'uint16', 'version', 'Software version of the EXE that created this file. If the SigmaMPL.exe version is 3.00 then this value would be 300.', None, ['profile']],
    ['year', 'uint16'],
    ['month', 'uint16'],
    ['day', 'uint16'],
    ['hours', 'uint16'],
    ['minutes', 'uint16'],
    ['seconds', 'uint16'],
    ['shots_sum', 'uint32', 'shots sum', 'Number of laser shots collected.', 'count', ['profile']],
    ['trigger_frequency', 'int32', 'trigger frequency', 'Laser fire rate (usually 2500).', 'Hz', ['profile']],
    ['energy_monitor', 'uint32', 'energy monitor', 'Mean of the Energy Monitor readings * 1000.', 'mJ', ['profile']],
    ['temp_0', 'uint32', 'A/D #0 mean', 'Mean of the A/D #0 readings * 100.', None, ['profile']],
    ['temp_1', 'uint32', 'A/D #1 mean', 'Mean of the A/D #1 readings * 100.', None, ['profile']],
    ['temp_2', 'uint32', 'A/D #2 mean', 'Mean of the A/D #2 readings * 100.', None, ['profile']],
    ['temp_3', 'uint32', 'A/D #3 mean', 'Mean of the A/D #3 readings * 100.', None, ['profile']],
    ['temp_4', 'uint32', 'A/D #4 mean', 'Mean of the A/D #4 readings * 100.', None, ['profile']],
    ['background_average', 'float32', 'background average', 'Background Average for Channel #1.', 'count us-1', ['profile']],
    ['background_stddev', 'float32', 'background standard deviation', 'Background Standard Deviation for channel #1.', 'count us-1', ['profile']],
    ['number_channels', 'uint16', 'number of channels', 'MCS Channels collected. Either 1 or 2.', 'count', ['profile']],
    ['number_bins', 'uint32'],
    ['bin_time', 'float32', 'bin time', 'Bin width (100, 200, or 500 nanoseconds).', 's', ['profile']],
    ['range_calibration', 'float32', 'range calibration', 'Default is 0; will indicate range calibration offset measured for particular unit.', 'm', ['profile']],
    ['number_data_bins', 'uint16', 'number of data bins', 'Number of data bins (not background) following First Data Bin.', 'count', ['profile']],
    ['scan_scenario_flags', 'uint16', 'scan scenario flags', '0: No scan scenario used, 1: Scan scenario used].', None, ['profile']],
    ['num_background_bins', 'uint16', 'number of background bins', 'Number of background bins following First Background Bin.', 'count', ['profile']],
    ['azimuth_angle', 'float32', 'azimuth angle', 'Azimuth angle of scanner.', 'degrees', ['profile']],
    ['elevation_angle', 'float32', 'elevation angle', 'Elevation angle of scanner.', 'degrees', ['profile']],
    ['compass_degrees', 'float32', 'compass degrees', 'Compass degrees (currently unused).', 'degrees', ['profile']],
    ['polarization_voltage_0', 'float32', 'polarization voltage 0', 'Not used.', None, ['profile']],
    ['polarization_voltage_1', 'float32', 'polarization voltage 1', 'Not used.', None, ['profile']],
    ['gps_latitude', 'float32', 'GPS latitude', 'GPS latitude (optional).', 'degrees_north', ['profile']],
    ['gps_longitude', 'float32', 'GPS longitude', 'GPS longitude (optional).', 'degrees_east', ['profile']],
    ['gps_altitude', 'float32', 'GPS altitude', 'GPS altitude (optional).', 'm', ['profile']],
    ['ad_data_bad_flag', 'uint8', 'A/D data bad flag', '0: A/D data good, 1: A/D data probably out of sync. Energy monitor collection is not exactly aligned with MCS shots.', None, ['profile']],
    ['data_file_version', 'uint8', 'data file version', 'Version of the file format.', None, ['profile']],
    ['background_average_2', 'float32', 'background average (channel 2)', 'Background Average for Channel #2.', 'count us-1', ['profile']],
    ['background_stddev_2', 'float32', 'background standard deviation (channel 2)', 'Background Standard Deviation for Channel #2.', 'count us-1', ['profile']],
    ['mcs_mode', 'uint8', 'MCS mode', 'MCS mode register.', None, ['profile']],
    ['first_data_bin', 'uint16', 'first data bin', 'Bin # of the first return data.', None, ['profile']],
    ['system_type', 'uint8', 'system type', '0: Normal MPL, 1: MiniMPL.', None, ['profile']],
    ['sync_pulses_seen_per_second', 'uint16', 'sync pulses seen per second', 'MiniMPL Only; indicates average number of laser pulses seen to validate if laser is operating correctly.', 'count s-1', ['profile']],
    ['first_background_bin', 'uint16', 'first background bin', 'Used primarily for MiniMPL (will always be 0 for normal MPL as background is collected pre-trigger).', None, ['profile']],
    ['header_size', 'uint16'],
    ['ws_used', 'uint8', 'weather station used', '0: Weather station not used, 1: Weather station used.', None, ['profile']],
    ['ws_inside_temp', 'float32', 'inside temperature', 'Weather station inside temperature.', 'degree_C', ['profile']],
    ['ws_outside_temp', 'float32', 'outside temperature', 'Weather station outside temperature.', 'degree_C', ['profile']],
    ['ws_inside_humidity', 'float32', 'inside humidity', 'Weather station inside humidity.', 'percent', ['profile']],
    ['ws_outside_humidity', 'float32', 'outside humidity', 'Weather station outside humidity.', 'percent', ['profile']],
    ['ws_dewpoint', 'float32', 'dewpoint temperature', 'Weather station dewpoint.', 'degree_C', ['profile']],
    ['ws_wind_speed', 'float32', 'wind speed', 'Weather station wind speed.', 'km h-1', ['profile']],
    ['ws_wind_direction', 'int16', 'wind direction', 'Weather station wind direction.', 'degree', ['profile']],
    ['ws_barometric_pressure', 'float32', 'barometric pressure', 'Weather station barometric pressure.', 'hPa', ['profile']],
    ['ws_rain_rate', 'float32', 'rain rate', 'Weather station rain rate.', 'mm h-1', ['profile']],
]

HEADER_AFTERPULSE = [
    ['ap_header', 'uint32', 'afterpulse header'],
    ['ap_file_version', 'uint16', 'afterpulse file version'],
    ['ap_number_channels', 'uint8', 'afterpulse number of channels', None, 'count'],
    ['ap_number_bins', 'uint32', 'afterpulse number of bins', None, 'count'],
    ['ap_energy', 'float64', 'afterpulse energy', None, 'uJ'],
    ['ap_background_average_copol', 'float64', 'afterpulse co pol background average', 'count us-1'],
    ['ap_background_average_crosspol', 'float64', 'afterpulse cross pol background average', 'count us-1'],
]

HEADER_TYPES = {x[0]: x[1] for x in HEADER_MPL}
HEADER_TYPES['channel_1'] = 'float32'
HEADER_TYPES['channel_2'] = 'float32'

EXCL_FIELDS = [
    'year',
    'month',
    'day',
    'hours',
    'minutes',
    'seconds',
    'header_size',
    'number_bins',
]

HEADER_FIELDS = [x[0] for x in HEADER_MPL]
FIELDS = [x for x in HEADER_FIELDS if x not in EXCL_FIELDS]

EXTRA_FIELDS = [
    ['ap_copol', 'float64', 'afterpulse co pol values', None, 'count us-1', ['ap_range']],
    ['ap_crosspol', 'float64', 'afterpulse cross pol values', None, 'count us-1', ['ap_range']],
    ['ap_range', 'float64', 'afterpulse range', None, 'km', ['ap_range']],
    ['c', 'float64', 'speed of light', None, 'm s-1'],
    ['channel_1', 'float32', 'channel #1 data', 'For MPL systems without POL-FS option, the return signal array is stored here. For MPL systems with the POL-FS option, the cross-polarized return signal array is stored here.', 'count us-1', ['profile', 'range']],
    ['channel_2', 'float32', 'channel #2 data', 'Used only with POL-FS option. The co-polarized return signal array is stored here.', 'count us-1', ['profile', 'range']],
    ['ol_number_bins', 'uint32', 'overlap number of bins', None, 'count'],
    ['dt_number_coeff', 'uint32', 'dead time number of coefficients', None, 'count'],
    ['ol_overlap', 'float64', 'overlap values', None, None, ['ol_range']],
    ['ol_range', 'float64', 'overlap range', None, 'km', ['ol_range']],
    ['dt_coeff', 'float32', 'dead time coefficient', 'N coefficients of polynomial degree N-1 in decreasing order', None, ['dt_coeff_degree']],
    ['dt_coeff_degree', 'uint32', 'dead time coefficient degree', None, 'count', ['dt_coeff_degree']],
    ['nrb_copol', 'float64', 'copol normalized relative backscatter', 'Experimental.', 'count us-1 uJ-1 km2', ['profile', 'range']],
    ['nrb_crosspol', 'float64', 'crosspol normalized relative backscatter', 'Experimental.', 'count us-1 uJ-1 km2', ['profile', 'range']],
    ['time', 'uint64', 'time', 'Record collection time.', 'seconds since 1970-01-01 00:00:00', ['profile']],
    ['time_utc', 'S19', 'UTC time', 'Record collection time (UTC).', 'ISO 8601', ['profile']],
]

NC_HEADER = {x[0]: {
        'dtype': x[1] if len(x) > 1 else None,
        'long_name': x[2] if len(x) > 2 else None,
        'comment': x[3] if len(x) > 3 else None,
        'units': x[4] if len(x) > 4 else None,
        'dims': x[5] if len(x) > 5 else [],
    }
    for x in (HEADER_MPL + HEADER_AFTERPULSE + EXTRA_FIELDS)
}

def read_header(f, header_dsc):
    types = [x[1] for x in header_dsc]
    fmt = '<' + ''.join([TYPES[x[1]] for x in header_dsc])
    size = struct.calcsize(fmt)
    fields = [x[0] for x in header_dsc]
    buf = f.read(size)
    if len(buf) == 0:
        return None
    if len(buf) < size:
        raise IOError('Incomplete header')
    res = struct.unpack_from(fmt, buf)
    return {k: np.array(v, dtype=t) for k, v, t in zip(fields, res, types)}

def read_afterpulse(f):
    d = read_header(f, HEADER_AFTERPULSE)
    if d['ap_header'] != 0xAAEEEEAA:
        raise IOError('Invalid afterpulse header')
    n = int(d['ap_number_bins'])
    for x in ['ap_range', 'ap_copol', 'ap_crosspol']:
        buf = f.read(8*n)
        if len(buf) < 8*n:
            raise IOError('Incomplete %s data' % x)
        a = struct.unpack_from('<' + 'd'*n, buf)
        d[x] = np.array(a, np.float64)
    return d

def read_overlap(f):
    buf = f.read()
    n = len(buf)//16
    f.seek(0)
    d = {'ol_number_bins': np.array(n, np.uint32)}
    for x in ['ol_range', 'ol_overlap']:
        buf = f.read(8*n)
        if len(buf) < 8*n:
            raise IOError('Incomplete %s data' % x)
        a = struct.unpack_from('<' + 'd'*n, buf)
        d[x] = np.array(a, np.float64)
    return d

def read_dead_time(f):
    buf = f.read()
    n = len(buf)//4
    d = {'dt_number_coeff': np.array(n, np.uint32)}
    a = struct.unpack_from('<' + 'f'*n, buf)
    d['dt_coeff'] = np.array(a, np.float32)
    d['dt_coeff_degree'] = np.arange(n - 1, -1, -1, dtype=np.uint32)
    return d

def read_mpl_profile(f):
    d = read_header(f, HEADER_MPL)
    if d is None:
        return None
    n = int(d['number_bins'])
    for x in ['channel_1', 'channel_2']:
        buf = f.read(4*n)
        if len(buf) < 4*n:
            raise IOError('Incomplete %s data' % x)
        a = struct.unpack_from('<' + 'f'*n, buf)
        d[x] = np.array(a, dtype=np.float32)
    return d

def time_utc(d):
    return '%04d-%02d-%02dT%02d:%02d:%02d' % (
        d['year'],
        d['month'],
        d['day'],
        d['hours'],
        d['minutes'],
        d['seconds'],
    )

def time(d):
    t = dt.datetime(d['year'], d['month'], d['day'], d['hours'], d['minutes'],
        d['seconds'])
    t0 = dt.datetime(1970, 1, 1)
    return (t - t0).total_seconds()

def calc_dtcf(x, coeff):
    n = len(coeff)
    return np.sum([(x*1e3)**(n-i-1)*coeff[i] for i in range(n)], axis=0)

def calc_nrb(d, channel, name, name2):
    raw = d[channel]
    n, m = raw.shape
    background = d['background_average' + name2]
    ap = d.get('ap' + name, np.zeros(m, np.float64))
    energy = d['energy_monitor']*1e-3
    ap_energy = d.get('ap_energy', 1.)
    ap_background = d.get('ap_background_average' + name, 0.)
    ol_range = d.get('ol_range')
    ap_range = d.get('ap_range')
    overlap = d.get('ol_overlap', np.ones(m, np.float64))
    dt_coeff = d.get('dt_coeff', np.array([1.]))

    nrb = np.full((n, m), np.nan, np.float64)

    for i in range(n):
        range_ = 0.5*d['bin_time'][i]*C*(np.arange(m) + 0.5)*1e-3
        ap2 = np.interp(range_, ap_range, ap) if ap_range is not None else ap
        overlap2 = np.interp(range_, ol_range, overlap) if ol_range is not None else overlap
        nrb[i] = (raw[i,:]*calc_dtcf(raw[i,:], dt_coeff) - \
            background[i]*calc_dtcf(background[i], dt_coeff) - \
            ap2*calc_dtcf(ap2, dt_coeff)*energy[i]/ap_energy + \
            ap_background*calc_dtcf(ap_background, dt_coeff)*energy[i]/ap_energy)* \
            range_**2/(overlap2*energy[i])

    return nrb

def process_mpl(dd):
    dx = {}
    for k in FIELDS:
        dx[k] = np.array([d[k] for d in dd], dtype=HEADER_TYPES[k])
    dx['channel_1'] = np.vstack(
        [np.array(d['channel_1'], dtype=np.float32) for d in dd]
    )
    dx['channel_2'] = np.vstack(
        [np.array(d['channel_2'], dtype=np.float32) for d in dd]
    )
    dx['time_utc'] = np.array([time_utc(d) for d in dd])
    dx['time'] = np.array([time(d) for d in dd], dtype=np.uint64)
    dx['c'] = C
    return dx

def process_nrb(d):
    d['nrb_copol'] = calc_nrb(d, 'channel_2', '_copol', '_2')
    d['nrb_crosspol'] = calc_nrb(d, 'channel_1', '_crosspol', '')
    return d

def read_mpl(filename):
    dd = []
    with open(filename, 'rb') as f:
        while True:
            d = read_mpl_profile(f)
            if d is None:
                break
            dd.append(d)
    return process_mpl(dd)

def write(d, filename):
    f = Dataset(filename, 'w')
    f.createDimension('profile', None)
    f.createDimension('range', None)
    f.createDimension('ap_range', None)
    f.createDimension('ol_range', None)
    f.createDimension('dt_coeff_degree', None)
    for k, v in d.items():
        h = NC_HEADER[k]
        var = f.createVariable(k, NC_TYPE[h['dtype']], h['dims'],
            fill_value=FILL_VALUE[h['dtype']])
        var[::] = v
        if h['units'] is not None: var.units = h['units']
        if h['long_name'] is not None: var.long_name = h['long_name']
        if h['comment'] is not None: var.comment = h['comment']
    f.created = dt.datetime.utcnow().strftime('%Y-%m-%dT:%H:%M:%SZ')
    f.software = 'mpl2nc (https://github.com/peterkuma/mpl2nc)'
    f.version = __version__
    f.close()

def main():
    p = argparse.ArgumentParser(prog='mpl2nc',
        description='Convert Sigma Space Micro Pulse Lidar (MPL) data files to NetCDF.'
    )
    p.add_argument('-a', nargs=1, dest='afterpulse',
        help='afterpulse (bin)')
    p.add_argument('-d', nargs=1, dest='dead_time',
        help='dead time correction (bin)')
    p.add_argument('-o', nargs=1, dest='overlap',
        help='overlap correction (bin)')
    p.add_argument('-q', dest='quiet', action='store_true',
        help='run quietly (suppress output)')
    p.add_argument('-v', action='version', version=__version__)
    p.add_argument('input', help='input file or directory (mpl)', nargs='?')
    p.add_argument('output', help='output file or directory (NetCDF)')

    args = p.parse_args()

    if args.input is None and \
        args.afterpulse is None and \
        args.overlap is None and \
        args.dead_time is None:
        sys.stderr.write('mpl2nc: at least one correction file or input have to be specified\n')
        sys.exit(1)

    afterpulse = None
    overlap = None
    dead_time = None

    if args.afterpulse is not None:
        with open(args.afterpulse[0], 'rb') as f:
            afterpulse = read_afterpulse(f)

    if args.overlap is not None:
        with open(args.overlap[0], 'rb') as f:
            overlap = read_overlap(f)

    if args.dead_time is not None:
        with open(args.dead_time[0], 'rb') as f:
            dead_time = read_dead_time(f)

    d = {}
    if afterpulse is not None:
        d.update(afterpulse)
    if overlap is not None:
        d.update(overlap)
    if dead_time is not None:
        d.update(dead_time)

    if args.input is None:
        write(d, args.output)
    else:
        if os.path.isdir(args.input):
            for name in sorted(os.listdir(args.input)):
                filename = os.path.join(args.input, name)
                output_filename = os.path.join(
                    args.output,
                    os.path.splitext(name)[0] + '.nc'
                )
                if not args.quiet:
                    print(filename)
                mpl = read_mpl(filename)
                mpl.update(d)
                process_nrb(mpl)
                write(mpl, output_filename)
        else:
            mpl = read_mpl(args.input)
            mpl.update(d)
            process_nrb(mpl)
            write(mpl, args.output)

if __name__ == '__main__':
    main()
