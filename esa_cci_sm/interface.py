# -*- coding: utf-8 -*-

import warnings
import numpy as np
import os

from pygeobase.io_base import ImageBase, MultiTemporalImageBase
from pygeobase.object_base import Image

from pynetcf.time_series import GriddedNcOrthoMultiTs
from pygeogrids.netcdf import load_grid

from datetime import timedelta

from esa_cci_sm.grid import CCI025Cellgrid
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

    def __init__(self, filename, mode='r', parameter='sm', array_1D=False):
        super(CCI_SM_025Img, self).__init__(filename, mode=mode)

        if type(parameter) != list:
            parameter = [parameter]
        self.parameters = parameter
        self.grid = CCI025Cellgrid()
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
                param_data = dataset.variables[parameter][:]
                param_data = np.flipud(param_data[0,:,:]).flatten()
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
            for key in return_img:
                return_img[key] = np.flipud(
                    return_img[key].reshape((720, 1440)))

            return Image(
                (self.grid.activearrlon.reshape((720, 1440))),
                np.flipud(self.grid.activearrlat.reshape((720, 1440))),
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

    def __init__(self, data_path, parameter='sm', array_1D=False):

        ioclass_kws = {'parameter': parameter,
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
        img_offsets = np.array([timedelta(hours=0),
                                timedelta(hours=3),
                                timedelta(hours=6),
                                timedelta(hours=9),
                                timedelta(hours=12),
                                timedelta(hours=15),
                                timedelta(hours=18),
                                timedelta(hours=21)])

        timestamps = []
        diff = end_date - start_date
        for i in range(diff.days + 1):
            daily_dates = start_date + timedelta(days=i) + img_offsets
            timestamps.extend(daily_dates.tolist())

        return timestamps

class CCITs(GriddedNcOrthoMultiTs):
    ''' Read ESA CCI SM netcdf file in time series format'''
    def __init__(self, ts_path, grid_path=None):
        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = load_grid(grid_path)
        super(CCITs, self).__init__(ts_path, grid)