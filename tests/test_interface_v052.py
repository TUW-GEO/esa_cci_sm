# -*- coding: utf-8 -*-
import os
from datetime import datetime
from esa_cci_sm.interface import CCI_SM_025Ds, CCI_SM_025Img
from esa_cci_sm.grid import CCILandGrid
import numpy as np
import numpy.testing as nptest

def test_CCI_SM_v052_025Ds_img_reading():
    """
    test for the reading of the CCI_SM_DS class
    """
    parameter = ['sm']
    data_path = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v05.2", "combined")
    img_c = CCI_SM_025Ds(data_path=data_path, parameter=parameter, subgrid=None,
                         array_1D=False)

    image_c = img_c.read(datetime(2016, 6, 7, 0))

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.timestamp == datetime(2016, 6, 7, 0)
    assert abs(image_c.data['sm'][273, 693] - 0.06405) <= 1e-3 ##
    assert image_c.lon.shape == image_c.lat.shape == (720, 1440)

    data_path = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v05.2", "active")
    img_a = CCI_SM_025Ds(data_path=data_path, parameter=parameter, subgrid=None,
                         array_1D=False)

    image_a = img_a.read(datetime(2016, 6, 6, 0))

    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert image_a.timestamp == datetime(2016, 6, 6, 0)
    assert abs(image_a.data['sm'][273, 693] - 0.65197) <= 1e-3

    assert image_a.lon.shape == image_a.lat.shape == (720, 1440)


    data_path = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v05.2", "passive")
    img_p = CCI_SM_025Ds(data_path=data_path, parameter=parameter, subgrid=None,
                         array_1D=False)

    image_p = img_p.read(datetime(2016, 6, 6, 0))

    assert sorted(image_p.data.keys()) == sorted(parameter)
    assert image_p.timestamp == datetime(2016, 6, 6, 0)
    assert abs(image_p.data['sm'][273, 693] - 0.0600) <= 1e-3
    assert image_p.lon.shape == image_p.lat.shape == (720, 1440)



def test_CCI_SM_v052_025Ds_timestamps_for_daterange():
    """
    test for the tstamps_for_daterange function of the CCI_SM_DS class
    """
    parameter = ['sm']
    should_datetime = [datetime(2016, 6, 6, 0),
                       datetime(2016, 6, 7, 0)]
    data_path = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v05.2", "active")
    img_a = CCI_SM_025Ds(data_path=data_path, parameter=parameter, subgrid=None,
        array_1D=True)

    tstamps_a = img_a.tstamps_for_daterange(datetime(2016, 6, 6),
                                            datetime(2016, 6, 7))

    assert len(tstamps_a) == 2
    assert tstamps_a == should_datetime

    data_path = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v05.2", "passive")

    img_p = CCI_SM_025Ds(data_path=data_path, parameter=parameter, subgrid=None,
                         array_1D=True)

    tstamps_p = img_p.tstamps_for_daterange(datetime(2016, 6, 6),
                                            datetime(2016, 6, 7))

    assert len(tstamps_p) == 2
    assert tstamps_p == should_datetime

    data_path = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                               "esa_cci_sm_dailyImages", "v02.2", "combined")
    img_c = CCI_SM_025Ds(data_path=data_path, parameter=parameter, subgrid=None,
                         array_1D=True)

    tstamps_c = img_c.tstamps_for_daterange(datetime(2016, 6, 7),
                                            datetime(2016, 6, 8))

    assert len(tstamps_c) == 2
    assert tstamps_c == [datetime(2016, 6, 7, 0),
                         datetime(2016, 6, 8, 0)]


def test_CCI_SM_v052_025Img_img_reading_1D_combined():
    """
    1D test for the read function of the CCI_SM_image class
    """

    ##### global grid
    parameter = ['sm']
    filename = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
                "esa_cci_sm_dailyImages", "v05.2", "combined", "2016",
                "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160607000000-fv05.2.nc")

    reader = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=None,
                          array_1D=True)

    image_c = reader.read()

    assert reader.grid.find_nearest_gpi(75.625, 14.625) == (602942, 0)

    ref_lat = image_c.lat[1440 * (719-301) + 1022]
    ref_lon = image_c.lon[1440 * (719-301) + 1022]

    assert ref_lon == 75.625
    assert ref_lat== 14.625
    assert sorted(image_c.data.keys()) == sorted(parameter)

    ref_sm = image_c.data['sm'][1440 * (719-301) + 1022]
    nptest.assert_almost_equal(ref_sm, 0.37016, 5)

    ###### land grid
    land_grid = CCILandGrid()
    img_c = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=land_grid,
                          array_1D=True)

    assert img_c.grid.find_nearest_gpi(75.625, 14.625) == (602942, 0)

    image_c = img_c.read()
    idx = np.where(land_grid.activegpis == 602942)[0][0]

    sm = image_c.data['sm'][idx]
    lat = image_c.lat[idx]
    lon = image_c.lon[idx]

    assert ref_lat == lat
    assert ref_lon == lon
    nptest.assert_almost_equal(ref_sm, sm, 5)



def test_CCI_SM_v052_025Img_img_reading_1D_active():
    parameter = ['sm']
    filename = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
               "esa_cci_sm_dailyImages", "v05.2", "active", "2016",
               "ESACCI-SOILMOISTURE-L3S-SSMS-ACTIVE-20160606000000-fv05.2.nc")

    img_a = CCI_SM_025Img(filename, parameter=parameter,  subgrid=None,
                          array_1D=True)

    image_a = img_a.read()

    assert img_a.grid.find_nearest_gpi(-6.625, 21.625) == (642933, 0)

    ref_lat = image_a.lat[1440 * (719-273) + 693]
    ref_lon = image_a.lon[1440 * (719-273) + 693]

    assert ref_lon == -6.625
    assert ref_lat== 21.625

    assert sorted(image_a.data.keys()) == sorted(parameter)

    ref_sm = image_a.data['sm'][1440 * (719-273) + 693]
    nptest.assert_almost_equal(ref_sm, 0.6519703, 5)

    ###### land grid
    land_grid = CCILandGrid()
    img_a = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=land_grid,
                          array_1D=True)

    assert img_a.grid.find_nearest_gpi(-6.625, 21.625) == (642933, 0)
    idx = np.where(land_grid.activegpis == 642933)[0][0]

    image_a = img_a.read()

    sm = image_a.data['sm'][idx]
    lat = image_a.lat[idx]
    lon = image_a.lon[idx]

    assert ref_lat == lat
    assert ref_lon == lon
    nptest.assert_almost_equal(ref_sm, sm, 5)


def test_CCI_SM_v052_025Img_img_reading_1D_passive():
    parameter = ['sm']
    filename = os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
               "esa_cci_sm_dailyImages", "v05.2", "passive", "2016",
               "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160606000000-fv05.2.nc")
    img_p = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=None,
                          array_1D=True)

    image_p = img_p.read()

    assert img_p.grid.find_nearest_gpi(-6.625, 21.625) == (642933, 0)

    ref_lat = image_p.lat[1440*(719-273)+693]
    ref_lon = image_p.lon[1440*(719-273)+693]

    assert ref_lon == -6.625
    assert ref_lat== 21.625

    assert sorted(image_p.data.keys()) == sorted(parameter)

    ref_sm = image_p.data['sm'][1440 * (719-273) + 693]
    nptest.assert_almost_equal(ref_sm, 0.0600, 5)

    ###### land grid
    land_grid = CCILandGrid()
    img_p = CCI_SM_025Img(filename=filename, parameter=parameter, subgrid=land_grid,
                          array_1D=True)

    assert img_p.grid.find_nearest_gpi(-6.625, 21.625) == (642933, 0)

    image_p = img_p.read()
    idx = np.where(land_grid.activegpis == 642933)[0][0]

    sm = image_p.data['sm'][idx]
    lat = image_p.lat[idx]
    lon = image_p.lon[idx]

    assert ref_lat == lat
    assert ref_lon == lon
    nptest.assert_almost_equal(ref_sm, sm, 5)

def test_CCI_SM_v052_025Img_img_reading_2D():
    """
    2D test for the read function of the CCI_SM_image class
    """
    parameter = ['sm']
    img_c = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v05.2", "combined", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20160607000000-fv05.2.nc"),
        parameter=parameter)

    image_c = img_c.read()

    assert sorted(image_c.data.keys()) == sorted(parameter)
    assert image_c.data['sm'].shape == (720, 1440)
    assert image_c.lon[0, 0] == -179.875
    assert image_c.lon[0, 1439] == 179.875
    assert image_c.lat[0, 0] == 89.875
    assert image_c.lat[719, 0] == -89.875
    assert abs(image_c.data['sm'][273, 693] - 0.06405) <= 1e-5
    assert image_c.lon.shape == image_c.lat.shape == (720, 1440)



    parameter = ['sm']
    img_a = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v05.2", "active", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMS-ACTIVE-20160606000000-fv05.2.nc"),
        parameter=parameter)

    image_a = img_a.read()

    assert sorted(image_a.data.keys()) == sorted(parameter)
    assert image_a.data['sm'].shape == (720, 1440)
    assert image_a.lon[0, 0] == -179.875
    assert image_a.lon[0, 1439] == 179.875
    assert image_a.lat[0, 0] == 89.875
    assert image_a.lat[719, 0] == -89.875
    assert abs(image_a.data['sm'][273, 693] - 0.65197) <= 1e-5
    assert image_a.lon.shape == image_a.lat.shape == (720, 1440)



    parameter = ['sm']
    img_p = CCI_SM_025Img(
        os.path.join(os.path.dirname(__file__), "esa_cci_sm-test-data",
        "esa_cci_sm_dailyImages", "v05.2", "passive", "2016",
        "ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20160606000000-fv05.2.nc"),
        parameter=parameter)

    image_p = img_p.read()

    assert sorted(image_p.data.keys()) == sorted(parameter)
    assert image_p.data['sm'].shape == (720, 1440)
    assert image_p.lon[0, 0] == -179.875
    assert image_p.lon[0, 1439] == 179.875
    assert image_p.lat[0, 0] == 89.875
    assert image_p.lat[719, 0] == -89.875
    assert abs(image_p.data['sm'][273, 693] - 0.0600) <= 1e-5
    assert image_p.lon.shape == image_p.lat.shape == (720, 1440)



if __name__ == '__main__':
    test_CCI_SM_v052_025Ds_img_reading()
    test_CCI_SM_v052_025Img_img_reading_2D()
    test_CCI_SM_v052_025Ds_timestamps_for_daterange()
    test_CCI_SM_v052_025Img_img_reading_1D_active()
    test_CCI_SM_v052_025Img_img_reading_1D_combined()
    test_CCI_SM_v052_025Img_img_reading_1D_passive()
