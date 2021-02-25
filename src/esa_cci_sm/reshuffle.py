# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2018 TU Wien
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

from repurpose.img2ts import Img2Ts
from esa_cci_sm.interface import CCI_SM_025Ds
from esa_cci_sm.grid import CCILandGrid, CCICellGrid

import configparser

from collections import OrderedDict

from netCDF4 import Dataset
import numpy as np


def str2bool(val):
    if val in ['True', 'true', 't', 'T', '1']:
        return True
    else:
        return False

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
    file_vars : list
        Names of parameters in the first detected file
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
                file_vars = Dataset(os.path.join(curr,f)).variables.keys()
                return file_args, file_vars

    raise IOError('No file name in passed directory fits to template')



def read_metadata(sensortype, version, varnames):
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

    Returns
    -------
    glob_meta : dict
        Global file metadata
    var_meta : dict
        Variable meta dicts
    '''
    config = configparser.RawConfigParser()
    config.optionxform = str
    metafile = os.path.join(os.path.dirname(__file__), 'metadata',
                            'esa_cci_sm_v0{}_{}.ini'.format(version,
                                                            sensortype.upper()))

    if not os.path.isfile(metafile):
        raise ValueError(metafile, 'Meta data file does not exist')

    config.read(metafile)

    global_meta = OrderedDict(config.items('GLOBAL'))

    var_meta = OrderedDict()
    for var in varnames:
        var_meta[var] = OrderedDict(config.items(var.upper()))
        try:
            delim = ',' if ',' in var_meta[var]['valid_range'] else ' '
            var_meta[var]['valid_range'] = \
                np.array([float(j) for j in var_meta[var]['valid_range'].split(delim)])
        except KeyError:
            pass

        try:
            fill_value = var_meta[var]['_FillValue']
            try:
                var_meta[var]['_FillValue'] = int(fill_value)
            except ValueError:
                var_meta[var]['_FillValue'] = float(fill_value)
        except KeyError:
            pass


    return global_meta, var_meta



def reshuffle(input_root, outputpath,
              startdate, enddate,
              parameters=None, land_points=True, ignore_meta=False,
              imgbuffer=200):
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
    land_points : bool, optional (default: True)
        Use the land grid to calculate time series on.
        Leads to faster processing and smaller files.
    imgbuffer: int, optional
        How many images to read at once before writing time series.
    """
    if land_points:
        grid = CCILandGrid()
    else:
        grid = CCICellGrid()

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    file_args, file_vars = parse_filename(input_root)

    if parameters is None:
        parameters = [p for p in file_vars if p not in ['lat', 'lon', 'time']]

    input_dataset = CCI_SM_025Ds(data_path=input_root, parameter=parameters,
                                 subgrid=grid, array_1D=True)

    if not ignore_meta:
        global_attr, ts_attributes = read_metadata(sensortype=file_args['sensor_type'],
                                                   version=int(file_args['version']),
                                                   varnames=parameters)
        global_attr['time_coverage_start'] = str(startdate)
        global_attr['time_coverage_end'] = str(enddate)
    else:
        global_attr = {'product' : 'ESA CCI SM'}
        ts_attributes = None


    reshuffler = Img2Ts(input_dataset=input_dataset, outputpath=outputpath,
                        startdate=startdate, enddate=enddate, input_grid=grid,
                        imgbuffer=imgbuffer, cellsize_lat=5.0, cellsize_lon=5.0,
                        global_attr=global_attr, zlib=True,
                        unlim_chunksize=1000, ts_attributes=ts_attributes)
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
    parser.add_argument("--parameters", metavar="parameters", default=None,
                        nargs="+",
                        help=("Parameters to reshuffle in numerical format. e.g."
                              "sm for Volumetric soil water layer. If None are passed"
                              "all variables in the image files are used"))

    parser.add_argument("--land_points", type=str2bool, default='False',
                        help=("Set True to convert only land points as defined"
                              " in the SMECV-grid land mask (faster and less/smaller files)"))
    parser.add_argument("--ignore_meta", type=str2bool, default='False',
                        help=("Do not apply metadata from ini files to the time series"))
    parser.add_argument("--imgbuffer", type=int, default=200,
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
              land_points=args.land_points,
              ignore_meta=args.ignore_meta,
              imgbuffer=args.imgbuffer)


def run():
    main(sys.argv[1:])



