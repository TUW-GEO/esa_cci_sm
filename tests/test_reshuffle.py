import os
import glob
import tempfile
import numpy as np
import numpy.testing as nptest

from esa_cci_sm.reshuffle import main
from esa_cci_sm.interface import CCITs


def test_reshuffle_v042():
    """
    test for the reshuffle function
    """
    inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "esa_cci_sm-test-data", "esa_cci_sm_dailyImages", "v04.2", "passive")
    startdate = "2016-06-06T00:00"
    enddate = "2016-06-07T00:00"
    parameters = ["sm"]
    ts_path = tempfile.mkdtemp()
    args = [inpath, ts_path, startdate, enddate] + parameters
    main(args)
    ds = CCITs(ts_path)
    assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == 2593
    assert ds.grid.find_nearest_gpi(-179.875, 68.375)[0] == 911520
    ts_1d = ds.read(911520)
    ts_2d = ds.read(-179.875, 68.375)  # 0031.nc
    ts_values_should = np.array([0.31, 0.40],
                                dtype=np.float32)
    nptest.assert_allclose(ts_1d['sm'].values,
                           ts_values_should, rtol=1e-5)
    nptest.assert_allclose(ts_2d['sm'].values,
                           ts_values_should, rtol=1e-5)


def test_reshuffle_v033():
    """
    test for the reshuffle function
    """
    inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "esa_cci_sm-test-data", "esa_cci_sm_dailyImages", "v03.3", "combined")
    startdate = "2016-01-01T00:00"
    enddate = "2016-01-03T00:00"
    parameters = ["sm"]
    ts_path = tempfile.mkdtemp()
    args = [inpath, ts_path, startdate, enddate] + parameters
    main(args)
    ds = CCITs(ts_path)
    assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == 2593
    assert ds.grid.find_nearest_gpi(-6.625, 39.125)[0] == 743733
    ts_1d = ds.read(743733)
    ts_2d = ds.read(-6.625, 39.125)  # 0031.nc
    ts_values_should = np.array([0.23484306, -9999.000],
                                dtype=np.float32)
    nptest.assert_allclose(ts_1d['sm'].values,
                           ts_values_should, rtol=1e-5)
    nptest.assert_allclose(ts_2d['sm'].values,
                           ts_values_should, rtol=1e-5)


def test_reshuffle_v022():
    """
    test for the reshuffle function
    """
    inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "esa_cci_sm-test-data", "esa_cci_sm_dailyImages", "v02.2",
                          "combined")
    startdate = "2014-01-01T00:00"
    enddate = "2014-01-02T00:00"
    parameters = ["sm"]
    ts_path = tempfile.mkdtemp()
    args = [inpath, ts_path, startdate, enddate] + parameters
    main(args)
    ds = CCITs(ts_path)
    assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == 2593
    assert ds.grid.find_nearest_gpi(-6.625, 21.625)[0] == 642933
    ts_1d = ds.read(642933)
    ts_2d = ds.read(-6.625, 21.625) # 0031.nc
    ts_values_should = np.array([0.1422, 0.1216],
                                dtype=np.float32)
    nptest.assert_allclose(ts_1d['sm'].values,
                           ts_values_should, rtol=1e-5)
    nptest.assert_allclose(ts_2d['sm'].values,
                           ts_values_should, rtol=1e-5)

