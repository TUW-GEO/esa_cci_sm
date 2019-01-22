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

import numpy as np
import os

from pygeobase.io_base import ImageBase, MultiTemporalImageBase
from pygeobase.object_base import Image

from pynetcf.time_series import GriddedNcOrthoMultiTs
from pygeogrids.netcdf import load_grid

from dateutil.relativedelta import relativedelta

from esa_cci_sm.grid import CCICellGrid
from netCDF4 import Dataset

class CCI_SM_025Img(ImageBase):
    """
    Class for reading one ESA CCI SM netcdf image file on a 0.25 DEG grid.

    Parameters
    ----------
    filename: string
        Filename of the ESA CCI SM netcdf file
    mode: string, optional (default: 'r')
        Mode of opening the file, only 'r' is implemented at the moment
    parameter : string or list, optional (default: 'sm')
        One or list of parameters to read, see ESA CCI documentation for
        more information
    array_1D: boolean, optional (default: False)
        If set then the data is read into 1D arrays. Needed for some legacy code.
    """

    def __init__(self, filename, mode='r', parameter='sm', subgrid=None,
                 array_1D=False):
        super(CCI_SM_025Img, self).__init__(filename, mode=mode)

        if type(parameter) != list:
            parameter = [parameter]
        self.parameters = parameter
        self.grid = CCICellGrid() if not subgrid else subgrid
        self.array_1D = array_1D

    def read(self, timestamp=None):
        # Returns the selected parameters for a ESA CCI SM image and according metadata
        return_img = {}
        return_metadata = {}

        try:
            dataset = Dataset(self.filename)
        except IOError as e:
            print(e)
            print(" ".join([self.filename, "can not be opened"]))
            raise e

        param_names = []
        for parameter in self.parameters:
            param_names.append(parameter)

        for parameter, variable in dataset.variables.items():
            if parameter in param_names:
                param_metadata = {}
                param_data = {}
                for attrname in variable.ncattrs():
                    if attrname in ['long_name', 'units']:
                        param_metadata.update(
                            {str(attrname): getattr(variable, attrname)})

                # param_data = dataset.variables[parameter][:].flatten()
                dataset.set_auto_mask(False)
                dataset.set_auto_scale(True)
                param_data = dataset.variables[parameter][:]
                param_data = np.flipud(param_data[0,:,:]).flatten()
                #param_data = param_data[0,:,:].flatten()
                np.ma.set_fill_value(param_data, 9999)

                return_img.update(
                    {str(parameter): param_data[self.grid.activegpis]})
                return_metadata.update({str(parameter): param_metadata})

                # Check for corrupt files
                try:
                    return_img[parameter]
                except KeyError:
                    path, thefile = os.path.split(self.filename)
                    print ('%s in %s is corrupt - filling image with NaN values' % (parameter, thefile))
                    return_img[parameter] = np.empty(self.grid.n_gpi).fill(np.nan)
                    return_metadata['corrupt_parameters'].append()

        dataset.close()
        if self.array_1D:
            return Image(self.grid.activearrlon, self.grid.activearrlat,
                         return_img, return_metadata, timestamp)
        else:
            yres, xres = self.grid.shape
            for key in return_img:
                return_img[key] = return_img[key].reshape((xres, yres))

            return Image(
                self.grid.activearrlon.reshape((xres, yres)),
                self.grid.activearrlat.reshape((xres, yres)),
                return_img,
                return_metadata,
                timestamp)

    def write(self, data):
        raise NotImplementedError()

    def flush(self):
        pass

    def close(self):
        pass

class CCI_SM_025Ds(MultiTemporalImageBase):
    """
    Class for reading ESA CCI SM images in nc format.

    Parameters
    ----------
    data_path : string
        Path to the nc image files
    parameter : string or list, optional (default: 'sm')
        One or list of parameters to read, see ESA CCI SM documentation
        for more information
    array_1D: boolean, optional (default: False)
        If set then the data is read into 1D arrays. Needed for some legacy code.
    """

    def __init__(self, data_path, parameter='sm', subgrid=None, array_1D=False):

        ioclass_kws = {'parameter': parameter,
                       'subgrid': subgrid,
                       'array_1D': array_1D}

        sub_path = ['%Y']
        filename_templ = "ESACCI-SOILMOISTURE-L3S-*-{datetime}-fv*.nc"
        super(CCI_SM_025Ds, self).__init__(data_path, CCI_SM_025Img,
                                                  fname_templ=filename_templ,
                                                  datetime_format="%Y%m%d%H%M%S",
                                                  subpath_templ=sub_path,
                                                  exact_templ=False,
                                                  ioclass_kws=ioclass_kws)

    def tstamps_for_daterange(self, start_date, end_date):
        """
        Return timestamps for the passed date range,

        Parameters
        ----------
        start_date: datetime
            start of date range
        end_date: datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """

        next = lambda date: date + relativedelta(days=1)

        timestamps = [start_date]
        while next(timestamps[-1]) <= end_date:
            timestamps.append(next(timestamps[-1]))

        return timestamps

class CCITs(GriddedNcOrthoMultiTs):
    def __init__(self, ts_path, grid_path=None, **kwargs):
        '''
        Class for reading ESA CCI SM time series after reshuffling.

        Parameters
        ----------
        ts_path : str
            Directory where the netcdf time series files are stored
        grid_path : str, optional (default: None)
            Path to grid file, that is used to organize the location of time
            series to read. If None is passed, grid.nc is searched for in the
            ts_path.

        Optional keyword arguments that are passed to the Gridded Base:
        ------------------------------------------------------------------------
            parameters : list, optional (default: None)
                Specific variable names to read, if None are selected, all are read.
            offsets : dict, optional (default:None)
                Offsets (values) that are added to the parameters (keys)
            scale_factors : dict, optional (default:None)
                Offset (value) that the parameters (key) is multiplied with
            ioclass_kws: dict
                Optional keyword arguments to pass to OrthoMultiTs class:
                ----------------------------------------------------------------
                    read_bulk : boolean, optional (default:False)
                        if set to True the data of all locations is read into memory,
                        and subsequent calls to read_ts read from the cache and not from disk
                        this makes reading complete files faster#
                    read_dates : boolean, optional (default:False)
                        if false dates will not be read automatically but only on specific
                        request useable for bulk reading because currently the netCDF
                        num2date routine is very slow for big datasets
        '''
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(CCITs, self).__init__(ts_path, grid, **kwargs)

