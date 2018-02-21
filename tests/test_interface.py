# -*- coding: utf-8 -*-
import os
from datetime import datetime

from hsaf_cci_042.interface import CCI_SM_v042_025Ds, CCI_SM_v042_025Img


def test_CCI_SM_v042_025Ds_img_reading():
    """
    test for the reading of the CCI_SM_v042_025Ds class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']

    img_a = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "active"), parameter=parameter,
        array_1D=True)

    image_a = img_a.read(
        datetime(2016, 6, 6, 0))

    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert image_a.timestamp == datetime(2016, 6, 6, 0)
    assert abs(image_a.data['sm'][133920] - 100) <= 1e-3
    assert image_a.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image_a.lon.shape == image_a.lat.shape

    img_p = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "passive"), parameter=parameter,
        array_1D=True)

    image_p = img_p.read(
        datetime(2016, 6, 6, 0))

    assert sorted(image_p.data.keys()) == sorted(parameter)
    assert image_p.timestamp == datetime(2016, 6, 6, 0)
    assert abs(image_p.data['sm'][123840] - 0.31) <= 1e-3
    assert image_p.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image_p.lon.shape == image_p.lat.shape

    img_c = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "combined"), parameter=parameter,
        array_1D=True)

    image_c = img_c.read(
        datetime(2016, 6, 7, 0))

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.timestamp == datetime(2016, 6, 7, 0)
    assert abs(image_c.data['sm'][122400] - 0.1755) <= 1e-3
    assert image_c.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image_c.lon.shape == image_c.lat.shape


def test_CCI_SM_v042_025Ds_timestamps_for_daterange():
    """
    test for the tstamps_for_daterange function of the CCI_SM_v042_025Ds class
    _a for active
    _p for passive
    _c for combined
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
    img_a = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "active"), parameter=parameter,
        array_1D=True)

    tstamps_a = img_a.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_a) == 8
    assert tstamps_a == should_datetime

    img_p = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
                               "esa_cci_sm_dailyImages", "passive"),
        parameter=parameter,
        array_1D=True)

    tstamps_p = img_p.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_p) == 8
    assert tstamps_p == should_datetime

    img_c = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
                               "esa_cci_sm_dailyImages", "combined"),
        parameter=parameter,
        array_1D=True)

    tstamps_c = img_c.tstamps_for_daterange(datetime(2016, 1, 1),
                                            datetime(2016, 1, 1))

    assert len(tstamps_c) == 8
    assert tstamps_c == should_datetime


def test_CCI_SM_v042_025Img_img_reading_1D():
    """
    1D test for the read function of the CCI_SM_v042_025Img class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']
    img_a = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "active", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMS-ACTIVE-20160606000000-fv04.2.nc"),
        parameter=parameter,
        array_1D=True)

    image_a = img_a.read()

    assert image_a.lon[133920] == -179.875
    assert image_a.lat[133920] == 66.625
    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert abs(image_a.data['sm'][133920] - 100) <= 1e-3

    img_p = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "passive", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160606000000-fv04.2.nc"),
        parameter=parameter,
        array_1D=True)

    image_p = img_p.read()

    assert image_p.lon[123840] == -179.875
    assert image_p.lat[123840] == 68.375
    assert sorted(image_p.data.keys()) == sorted(parameter)
    assert abs(image_p.data['sm'][123840] - 0.31) <= 1e-3

    img_c = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "combined", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160607000000-fv04.2.nc"),
        parameter=parameter,
        array_1D=True)

    image_c = img_c.read()

    assert image_c.lon[122400] == -179.875
    assert image_c.lat[122400] == 68.625
    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert abs(image_c.data['sm'][122400] - 0.1755) <= 1e-3

def test_CCI_SM_v042_025Img_img_reading_2D():
    """
    2D test for the read function of the CCI_SM_v042_025Img class
    _a for active
    _p for passive
    _c for combined
    """
    parameter = ['sm']
    img_a = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "active", "2016",
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

    img_p = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "passive", "2016",
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

    img_c = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "combined", "2016",
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

if __name__ == '__main__':
    test_CCI_SM_v042_025Ds_img_reading()
    test_CCI_SM_v042_025Ds_timestamps_for_daterange()
    test_CCI_SM_v042_025Img_img_reading_1D()
    test_CCI_SM_v042_025Img_img_reading_2D()


