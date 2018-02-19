# -*- coding: utf-8 -*-
import os
from datetime import datetime

from hsaf_cci_042.interface import CCI_SM_v042_025Ds, CCI_SM_v042_025Img


def test_CCI_SM_v042_025Ds_img_reading():
    """
    test for the reading of the CCI_SM_v042_025Ds class
    """
    parameter = ['sm']
    img = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "passive"), parameter=parameter,
        array_1D=True)

    image = img.read(
        datetime(2016, 6, 6, 0))

    assert image.timestamp == datetime(2016, 6, 6, 0)
    assert round(image.data['sm'][123840], 3) == 0.31
    assert image.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image.lon.shape == image.lat.shape


def test_CCI_SM_v042_025Ds_timestamps_for_daterange():
    """
    test for the tstamps_for_daterange function of the CCI_SM_v042_025Ds class
    """
    parameter = ['sm']
    img = CCI_SM_v042_025Ds(
        data_path=os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "passive"), parameter=parameter,
        array_1D=True)

    tstamps = img.tstamps_for_daterange(datetime(2016, 1, 1),
                                        datetime(2016, 1, 1))
    assert len(tstamps) == 8
    assert tstamps == [datetime(2016, 1, 1, 0),
                       datetime(2016, 1, 1, 3),
                       datetime(2016, 1, 1, 6),
                       datetime(2016, 1, 1, 9),
                       datetime(2016, 1, 1, 12),
                       datetime(2016, 1, 1, 15),
                       datetime(2016, 1, 1, 18),
                       datetime(2016, 1, 1, 21)]


def test_CCI_SM_v042_025Img_img_reading_1D():
    """
    1D test for the read function of the CCI_SM_v042_025Img class
    """
    parameter = ['sm']
    img = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "passive", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160606000000-fv04.2.nc"),
        parameter=parameter,
        array_1D=True)

    image = img.read()
    assert round(image.data['sm'][122486],3) == 0.31


def test_CCI_SM_v042_025Img_img_reading_2D():
    """
    2D (lat, long) test for the read function of the CCI_SM_v042_025Img class
    """
    parameter = ['sm']
    img = CCI_SM_v042_025Img(
        os.path.join(os.path.dirname(__file__), "hsaf_cci_042_data",
        "esa_cci_sm_dailyImages", "passive", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160606000000-fv04.2.nc"),
        parameter=parameter)

    image = img.read()

    assert image.data['sm'].shape == (720, 1440)
    assert image.lon[0, 0] == -179.875
    assert image.lon[0, 1439] == 179.875
    assert image.lat[0, 0] == 89.875
    assert image.lat[719, 0] == -89.875
    assert sorted(image.data.keys()) == sorted(parameter)
    assert round(image.data['sm'][86, 0], 3) == 0.31
    # print(image.lon[86, 0])
    # print(image.lat[86, 0])
    assert image.lon.shape == (720, 1440)
    assert image.lon.shape == image.lat.shape


if __name__ == '__main__':
    test_CCI_SM_v042_025Ds_img_reading()
    test_CCI_SM_v042_025Ds_timestamps_for_daterange()
    test_CCI_SM_v042_025Img_img_reading_1D()
    test_CCI_SM_v042_025Img_img_reading_2D()


