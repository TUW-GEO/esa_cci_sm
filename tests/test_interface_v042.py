# -*- coding: utf-8 -*-
import os
from datetime import datetime

from esa_cci_sm.interface import CCI_SM_025Ds, CCI_SM_025Img
from esa_cci_sm.grid import CCILandGrid

import numpy.testing as nptest

def test_CCI_SM_v042_025Ds_img_reading():
    """
    test for the reading of the CCI_SM_v042_025Ds class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']

    data_path = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                             "esa_cci_sm_dailyImages", "v04.2", "combined")

    img_c = CCI_SM_025Ds(data_path=data_path, parameter=parameter, subgrid=None,
        array_1D=True)

    image_c = img_c.read(datetime(2016, 6, 7, 0))

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.timestamp == datetime(2016, 6, 7, 0)
    assert abs(image_c.data['sm'][122400] - 0.1755) <= 1e-3 # 1440 * 85 = 1222400
    assert image_c.lon.shape == image_c.lat.shape == (720 * 1440,)


    img_a = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v04.2", "active"), parameter=parameter,
        array_1D=True)

    image_a = img_a.read(
        datetime(2016, 6, 6, 0))

    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert image_a.timestamp == datetime(2016, 6, 6, 0)
    assert abs(image_a.data['sm'][133920] - 100) <= 1e-3 # 93*1440
    assert image_a.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image_a.lon.shape == image_a.lat.shape

    img_p = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v04.2", "passive"), parameter=parameter,
        array_1D=True)

    image_p = img_p.read(
        datetime(2016, 6, 6, 0))

    assert sorted(image_p.data.keys()) == sorted(parameter)
    assert image_p.timestamp == datetime(2016, 6, 6, 0)
    assert abs(image_p.data['sm'][123840] - 0.31) <= 1e-3 # 86*1440
    assert image_p.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image_p.lon.shape == image_p.lat.shape




def test_CCI_SM_v042_025Ds_timestamps_for_daterange():
    """
    test for the tstamps_for_daterange function of the CCI_SM_v042_025Ds class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']
    should_datetime = [datetime(2016, 1, 1, 0)]
    img_a = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v04.2", "active"), parameter=parameter,
        array_1D=True)

    tstamps_a = img_a.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_a) == 1
    assert tstamps_a == should_datetime

    img_p = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                               "esa_cci_sm_dailyImages", "v04.2", "passive"),
        parameter=parameter,
        array_1D=True)

    tstamps_p = img_p.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_p) == 1
    assert tstamps_p == should_datetime

    img_c = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                               "esa_cci_sm_dailyImages", "v04.2", "combined"),
        parameter=parameter,
        array_1D=True)

    tstamps_c = img_c.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_c) == 1
    assert tstamps_c == should_datetime


def test_CCI_SM_v042_025Img_img_reading_1D_combined():
    """
    1D test for the read function of the CCI_SM_v042_025Img class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']
    filename = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v04.2", "combined", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160607000000-fv04.2.nc")

    img_c = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=None,
                          array_1D=True)

    image_c = img_c.read()


    ref_lat = image_c.lat[1440 * 85] # = 122400
    ref_lon = image_c.lon[1440 * 85]

    assert ref_lon == -179.875
    assert ref_lat == 68.625
    assert sorted(image_c.data.keys()) == sorted(parameter)
    ref_sm = image_c.data['sm'][122400]
    assert abs(ref_sm - 0.1755) <= 1e-3

    ###land_grid
    land_grid = CCILandGrid()
    img_c = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=land_grid,
                          array_1D=True)

    assert img_c.grid.find_nearest_gpi(-179.875, 68.625) == (912960, 0)

    image_c = img_c.read()

    sm = image_c.data['sm'][24434]
    lat = image_c.lat[24434]
    lon = image_c.lon[24434]

    assert ref_lat == lat
    assert ref_lon == lon
    nptest.assert_almost_equal(ref_sm, sm, 5)

def test_CCI_SM_v042_025Img_img_reading_1D_active():
    """
    1D test for the read function of the CCI_SM_v042_025Img class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']
    filename = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v04.2", "active", "2016",
                "ESACCI-SOILMOISTURE-L3S-SSMS-ACTIVE-20160606000000-fv04.2.nc")


    img_a = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=None,
                          array_1D=True)

    image_a = img_a.read()

    ref_lat = image_a.lat[1440 * 93]  # = 133920
    ref_lon = image_a.lon[1440 * 93]

    assert ref_lon == -179.875
    assert ref_lat == 66.625
    assert sorted(image_a.data.keys()) == sorted(parameter)
    ref_sm = image_a.data['sm'][133920]
    assert abs(ref_sm - 100.) <= 1e-3

    ###land_grid
    land_grid = CCILandGrid()
    img_a = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=land_grid,
                          array_1D=True)

    assert img_a.grid.find_nearest_gpi(-179.875, 66.625) == (901440, 0)

    image_a = img_a.read()

    sm = image_a.data['sm'][32830]
    lat = image_a.lat[32830]
    lon = image_a.lon[32830]

    assert ref_lat == lat
    assert ref_lon == lon
    nptest.assert_almost_equal(ref_sm, sm, 5)

def test_CCI_SM_v042_025Img_img_reading_1D_passive():

    parameter = ['sm']
    filename = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v04.2", "passive", "2016",
                "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160606000000-fv04.2.nc")

    img_p = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=None,
                          array_1D=True)

    image_p = img_p.read()

    ref_lat = image_p.lat[1440 * 86]  # = 123840
    ref_lon = image_p.lon[1440 * 86]

    assert ref_lon == -179.875
    assert ref_lat == 68.375
    assert sorted(image_p.data.keys()) == sorted(parameter)
    ref_sm = image_p.data['sm'][123840]
    assert abs(ref_sm - 0.31) <= 1e-3

    ###land_grid
    land_grid = CCILandGrid()
    img_a = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=land_grid,
                          array_1D=True)

    assert img_a.grid.find_nearest_gpi(-179.875, 68.375) == (911520, 0)

    image_a = img_a.read()

    sm = image_a.data['sm'][25410]
    lat = image_a.lat[25410]
    lon = image_a.lon[25410]

    assert ref_lat == lat
    assert ref_lon == lon
    nptest.assert_almost_equal(ref_sm, sm, 5)



def test_CCI_SM_v042_025Img_img_reading_2D():
    """
    2D test for the read function of the CCI_SM_v042_025Img class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']

    img_c = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v04.2", "combined", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160607000000-fv04.2.nc"),
        parameter=parameter)

    image_c = img_c.read()

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.data['sm'].shape == (720, 1440)
    assert image_c.lon[0, 0] == -179.875
    assert image_c.lon[0, 1439] == 179.875
    assert image_c.lat[0, 0] == 89.875
    assert image_c.lat[719, 0] == -89.875
    assert image_c.lat[85, 0] == 68.625
    assert abs(image_c.data['sm'][85, 0] - 0.1755) <= 1e-3
    assert image_c.lon.shape == (720, 1440)
    assert image_c.lon.shape == image_c.lat.shape

    img_a = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v04.2", "active", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMS-ACTIVE-20160606000000-fv04.2.nc"),
        parameter=parameter)

    image_a = img_a.read()

    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert image_a.data['sm'].shape == (720, 1440)
    assert image_a.lon[0, 0] == -179.875
    assert image_a.lon[0, 1439] == 179.875
    assert image_a.lat[0, 0] == 89.875
    assert image_a.lat[719, 0] == -89.875
    assert abs(image_a.data['sm'][93, 0] - 100) <= 1e-3
    assert image_a.lon.shape == (720, 1440)
    assert image_a.lon.shape == image_a.lat.shape

    img_p = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v04.2", "passive", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160606000000-fv04.2.nc"),
        parameter=parameter)

    image_p = img_p.read()

    assert sorted(image_p.data.keys()) == sorted(parameter)
    assert image_p.data['sm'].shape == (720, 1440)
    assert image_p.lon[0, 0] == -179.875
    assert image_p.lon[0, 1439] == 179.875
    assert image_p.lat[0, 0] == 89.875
    assert image_p.lat[719, 0] == -89.875
    assert image_p.lon[86, 0] == -179.875
    assert image_p.lat[86, 0] == 68.375
    assert abs(image_p.data['sm'][86, 0] - 0.31) <= 1e-3
    assert image_p.lon.shape == (720, 1440)
    assert image_p.lon.shape == image_p.lat.shape



if __name__ == '__main__':
    test_CCI_SM_v042_025Img_img_reading_2D()

    test_CCI_SM_v042_025Ds_img_reading()
    test_CCI_SM_v042_025Ds_timestamps_for_daterange()
    test_CCI_SM_v042_025Img_img_reading_1D_combined()
    test_CCI_SM_v042_025Img_img_reading_1D_active()
    test_CCI_SM_v042_025Img_img_reading_1D_passive()


