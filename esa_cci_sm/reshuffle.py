# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2016, TU Wien
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Module for a command line interface to convert the ESACCI data into a
time series format using the repurpose package
'''

import os
import sys
import argparse
from parse import parse

from datetime import datetime

from pygeogrids import BasicGrid
from repurpose.img2ts import Img2Ts
from esa_cci_sm.interface import CCI_SM_025Ds

try:
    import ConfigParser as configparser
except ImportError:
    import configparser as configparser

from collections import OrderedDict

from netCDF4 import Dataset


def mkdate(datestring):
    if len(datestring) == 10:
        return datetime.strptime(datestring, '%Y-%m-%d')
    if len(datestring) == 16:
        return datetime.strptime(datestring, '%Y-%m-%dT%H:%M')


def parse_filename(data_dir):
    '''
    Take the first file in the passed directory and use its file name to
    retrieve the product type, version number and variables in the file.

    Parameters
    ----------
    inroot : str
        Input root directory

    Returns
    -------
    file_args : dict
        Parsed arguments from file name
    '''
    template = '{product}-SOILMOISTURE-L3S-{data_type}-{sensor_type}-' \
               '{datetime}000000-fv{version}.{sub_version}.nc'

    for curr, subdirs, files in os.walk(data_dir):
        for f in files:
            file_args = parse(template, f)
            if file_args is None:
                continue
            else:
                file_args = file_args.named
                file_args['datetime'] = '{datetime}'
                filevars = Dataset(os.path.join(curr,f)).variables.keys()
                return file_args, filevars

    raise IOError('No file name in passed directory fits to template')



def prod_spec_names(sensortype, subversion, config):
    '''
    Get specific names for sensortype version

    Parameters
    ----------
    sensortype str
        Product type: active, passive, combined
    subversion : str
        Subversion identifier. eg. '02'
    config : configparser.configparser
        config parser to replace values in

    Returns
    -------
    config : configparser.configparser
        The updated configuration parser
    '''

    sensor_abbr = {'ACTIVE': 'SSMS', 'PASSIVE': 'SSMV', 'COMBINED': 'SSMV'}

    sm_units_dict = {'ACTIVE': 'percentage (%)', 'PASSIVE': 'm3 m-3', 'COMBINED': 'm3 m-3'}

    sm_full_name_dict = {'ACTIVE': 'Percent of Saturation Soil Moisture',
                         'PASSIVE': 'Volumetric Soil Moisture',
                         'COMBINED': 'Volumetric Soil Moisture'}

    sm_uncertainty_full_name_dict = {'ACTIVE': 'Percent of Saturation Soil Moisture Uncertainty',
                                     'PASSIVE': 'Volumetric Soil Moisture Uncertainty',
                                     'COMBINED': 'Volumetric Soil Moisture Uncertainty'}

    sensortype = sensortype.upper()

    product = config.get('GLOBAL', 'product', 0,
                              {'sensor_abbr':sensor_abbr[sensortype.upper()],
                               'sensortype':sensortype,
                               'subversion':subversion})

    config.set('GLOBAL', 'product', product)

    config.set('SM', 'full_name', sm_full_name_dict[sensortype])
    config.set('SM', 'units', sm_units_dict[sensortype])


    config.set('SM_UNCERTAINTY', 'full_name', sm_uncertainty_full_name_dict[sensortype])
    config.set('SM_UNCERTAINTY', 'units', sm_units_dict[sensortype])

    return config


def read_metadata(sensortype, version, varnames, subversion):
    '''
    Read metadata dictionaries from the according ini file

    Parameters
    ----------
    sensortype : str
        product type: active, passive, combined
    version : int
        ESA CCI SM main version (eg. 2 or 3 or 4)
    varnames : list
        List of variables to read metadata for.
    subversion : str
        Subversion identifier. eg. '02'

    Returns
    -------
    glob_meta : dict
        Global file metadata
    var_meta : dict
        Variable meta dicts
    '''
    config = configparser.ConfigParser()
    metafile = os.path.join(os.path.dirname(__file__), 'metadata',
                            'esa_cci_sm_v0%i.ini' % version)

    if not os.path.isfile(metafile):
        raise ValueError(metafile, 'Meta data file does not exist')

    config.read(metafile)

    config = prod_spec_names(sensortype, subversion, config)

    global_meta = OrderedDict(config.items('GLOBAL'))

    var_meta = OrderedDict()
    for var in varnames:
        var_meta[var] = OrderedDict(config.items(var.upper()))

    return global_meta, var_meta



def reshuffle(input_root, outputpath,
              startdate, enddate,
              parameters=None, ignore_meta=False,
              imgbuffer=50):
    """
    Reshuffle method applied to ESA CCI SM images.

    Parameters
    ----------
    input_root: string
        input path where era interim data was downloaded
    outputpath : string
        Output path.
    startdate : datetime
        Start date.
    enddate : datetime
        End date.
    parameters: list, optional (default: None)
        parameters to read and convert
        If none are passed, we read an image in the root path and use vars from
        the image.
    imgbuffer: int, optional
        How many images to read at once before writing time series.
    """

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    file_args, file_vars = parse_filename(input_root)

    if parameters is None:
        parameters = [p for p in file_vars if p not in ['lat', 'lon', 'time']]

    input_dataset = CCI_SM_025Ds(input_root, parameters,
                                             array_1D=True)

    data = input_dataset.read(startdate)
    grid = BasicGrid(data.lon, data.lat)

    if not ignore_meta:
        global_attr, ts_attributes = read_metadata(sensortype=file_args['sensor_type'],
                                                   version=int(file_args['version']),
                                                   varnames=parameters,
                                                   subversion=file_args['sub_version'])
    else:
        global_attr = {'product' : 'ESA CCI SM'}
        ts_attributes = None


    reshuffler = Img2Ts(input_dataset=input_dataset, outputpath=outputpath,
                        startdate=startdate, enddate=enddate,
                        input_grid=grid,
                        imgbuffer=imgbuffer, cellsize_lat=5.0, cellsize_lon=5.0,
                        global_attr=global_attr,
                        zlib=True,
                        unlim_chunksize=1000,
                        ts_attributes=ts_attributes)
    reshuffler.calc()


def parse_args(args):
    '''
    Parse command line parameters for conversion from image to timeseries

    Parameters
    ----------
    args : list
        command line parameters as list of strings

    Returns
    -------
    params : argparse.Namespace
        Command line parameters
    '''

    parser = argparse.ArgumentParser(
        description="Convert ESA CCI image data to time series format.")
    parser.add_argument("dataset_root",
                        help='Root of local filesystem where the data is stored.')
    parser.add_argument("timeseries_root",
                        help='Root of local filesystem where the timeseries should be stored.')
    parser.add_argument("start", type=mkdate,
                        help=("Startdate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."))
    parser.add_argument("end", type=mkdate,
                        help=("Enddate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."))
    parser.add_argument("parameters", metavar="parameters", default=None,
                        nargs="+",
                        help=("Parameters to reshuffle in numerical format. e.g."
                              "sm for Volumetric soil water layer. If None are passed"
                              "all variables in the image files are used"))

    parser.add_argument("--ignore_meta", type=bool, default=False,
                        help=("Do not apply metadata from ini files to the time series"))
    parser.add_argument("--imgbuffer", type=int, default=50,
                        help=("How many images to read at once. Bigger numbers make the "
                              "conversion faster but consume more memory."))
    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse

    print("Converting data from {} to {} into folder {}.".format(args.start.isoformat(),
                                                                 args.end.isoformat(),
                                                                 args.timeseries_root))
    return args


def main(args):
    args = parse_args(args)

    reshuffle(args.dataset_root,
              args.timeseries_root,
              args.start,
              args.end,
              args.parameters,
              imgbuffer=args.imgbuffer)


def run():
    main(sys.argv[1:])

if __name__ == '__main__':
    inroot = r'H:\code\esa_cci_sm\tests\esa_cci_sm-test-data\esa_cci_sm_dailyImages\v04.2\combined'
    outpath = r'C:\Temp\ts'
    reshuffle(inroot, outpath,
              datetime(2016,6,7), datetime(2016,6,8),
              None, ignore_meta=False,
              imgbuffer=50)