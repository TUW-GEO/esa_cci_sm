import os
import glob
import tempfile
import numpy as np
import numpy.testing as nptest

from hsaf_cci_042.reshuffle import main
from hsaf_cci_042.interface import CCITs


def test_reshuffle():
    """
    test for the reshuffle function
    """
    inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "hsaf_cci_042_data", "esa_cci_sm_dailyImages", "passive")
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

if __name__ == '__main__':
    test_reshuffle()

