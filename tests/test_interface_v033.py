# -*- coding: utf-8 -*-
import os
from datetime import datetime

from esa_cci_sm.interface import CCI_SM_025Ds, CCI_SM_025Img

import numpy.testing as nptest

def test_CCI_SM_v033_025Ds_img_reading():
    """
    test for the reading of the CCI_SM_v033_025Ds class
    """
    parameter = ['sm']

    img_c = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "combined"), parameter=parameter,
        array_1D=False)

    image_c = img_c.read(
        datetime(2016, 1, 1, 0))

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.timestamp == datetime(2016, 1, 1, 0)
    nptest.assert_almost_equal(image_c.data['sm'][203, 693], 0.23484, 5)
    assert image_c.lon.shape == image_c.lat.shape == (720, 1440)


    img_a = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "active"), parameter=parameter,
        array_1D=False)

    image_a = img_a.read(
        datetime(2016, 1, 1, 0))

    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert image_a.timestamp == datetime(2016, 1, 1, 0)
    nptest.assert_almost_equal(image_a.data['sm'][203, 693], 67.70157, 5)
    assert image_c.lon.shape == image_c.lat.shape == (720, 1440)


    img_c = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "passive"), parameter=parameter,
        array_1D=False)

    image_c = img_c.read(
        datetime(2016, 1, 1, 0))

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.timestamp == datetime(2016, 1, 1, 0)
    nptest.assert_almost_equal(image_c.data['sm'][203, 693], 0.322685, 5)
    assert image_c.lon.shape == image_c.lat.shape == (720, 1440)



def test_CCI_SM_v033_025Ds_timestamps_for_daterange():
    """
    test for the tstamps_for_daterange function of the CCI_SM_v042_025Ds class
    """
    parameter = ['sm']
    should_datetime = [datetime(2016, 1, 1, 0),
                       datetime(2016, 1, 1, 3),
                       datetime(2016, 1, 1, 6),
                       datetime(2016, 1, 1, 9),
                       datetime(2016, 1, 1, 12),
                       datetime(2016, 1, 1, 15),
                       datetime(2016, 1, 1, 18),
                       datetime(2016, 1, 1, 21)]
    img_a = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "active"), parameter=parameter,
        array_1D=True)

    tstamps_a = img_a.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_a) == 8
    assert tstamps_a == should_datetime

    img_p = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
                               "esa_cci_sm_dailyImages", "v03.3", "passive"),
        parameter=parameter,
        array_1D=True)

    tstamps_p = img_p.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_p) == 8
    assert tstamps_p == should_datetime

    img_c = CCI_SM_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
                               "esa_cci_sm_dailyImages", "v03.3", "combined"),
        parameter=parameter,
        array_1D=True)

    tstamps_c = img_c.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_c) == 8
    assert tstamps_c == should_datetime


def test_CCI_SM_v033_025Img_img_reading_1D():
    """
    1D test for the read function of the CCI_SM_v042_025Img class
    """

    parameter = ['sm']
    img_c = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "combined", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160101000000-fv03.3.nc"),
        parameter=parameter, array_1D=True)

    image_c = img_c.read()

    assert image_c.lon[901440] == -179.875
    assert image_c.lat[901440] == 66.625
    assert sorted(image_c.data.keys()) == sorted(parameter)
    nptest.assert_almost_equal(image_c.data['sm'][1440 * (720 - 204) + 693],
                               0.23484, 5)



    parameter = ['sm']
    img_a = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "active", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMS-ACTIVE-20160101000000-fv03.3.nc"),
        parameter=parameter, array_1D=True)

    image_a = img_a.read()

    assert image_a.lon[901440] == -179.875
    assert image_a.lat[901440] == 66.625
    assert sorted(image_a.data.keys()) == sorted(parameter)
    nptest.assert_almost_equal(image_a.data['sm'][1440 * (720 - 204) + 693],
                               67.70157, 5)




    parameter = ['sm']
    img_p = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "passive", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160101000000-fv03.3.nc"),
        parameter=parameter, array_1D=True)

    image_p = img_p.read()

    assert image_p.lon[901440] == -179.875
    assert image_p.lat[901440] == 66.625
    assert sorted(image_p.data.keys()) == sorted(parameter)
    nptest.assert_almost_equal(image_p.data['sm'][1440 * (720 - 204) + 693],
                               0.322685, 5)

def test_CCI_SM_v33_025Img_img_reading_2D():
    """
    2D test for the read function of the CCI_SM_v042_025Img class
    """
    parameter = ['sm']
    img_c = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "combined", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160101000000-fv03.3.nc"),
        parameter=parameter)

    image_c = img_c.read()

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.data['sm'].shape == (720, 1440)
    assert image_c.lon[0, 0] == -179.875
    assert image_c.lon[0, 1439] == 179.875
    assert image_c.lat[0, 0] == 89.875
    assert image_c.lat[719, 0] == -89.875
    nptest.assert_almost_equal(image_c.data['sm'][203, 693], 0.23484, 5)
    assert image_c.lon.shape == image_c.lat.shape == (720, 1440)



    parameter = ['sm']
    img_a = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "active", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMS-ACTIVE-20160101000000-fv03.3.nc"),
        parameter=parameter)

    image_a = img_a.read()

    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert image_a.data['sm'].shape == (720, 1440)
    assert image_a.lon[0, 0] == -179.875
    assert image_a.lon[0, 1439] == 179.875
    assert image_a.lat[0, 0] == 89.875
    assert image_a.lat[719, 0] == -89.875
    nptest.assert_almost_equal(image_a.data['sm'][203, 693], 67.70157, 5)
    assert image_a.lon.shape == image_a.lat.shape == (720, 1440)



    parameter = ['sm']
    img_p = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "v03.3", "passive", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160101000000-fv03.3.nc"),
        parameter=parameter)

    image_p = img_p.read()

    assert sorted(image_p.data.keys()) == sorted(parameter)
    assert image_p.data['sm'].shape == (720, 1440)
    assert image_p.lon[0, 0] == -179.875
    assert image_p.lon[0, 1439] == 179.875
    assert image_p.lat[0, 0] == 89.875
    assert image_p.lat[719, 0] == -89.875
    nptest.assert_almost_equal(image_p.data['sm'][203, 693], 0.322685, 5)
    assert image_p.lon.shape == image_p.lat.shape == (720, 1440)




