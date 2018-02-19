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
    assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == 2593
    ds = CCITs(ts_path)
    # print(ds.read(123840))
    # print(ds.read(-179.875, 68.375))  # 0031.nc
    # ts = ds.read(40, 15)
    ts = ds.read(123840)
    ts_values_should = np.array([0.31, 0.40],
                                dtype=np.float32)
    nptest.assert_allclose(ts['sm'].values,
                           ts_values_should, rtol=1e-5)


if __name__ == '__main__':
    test_reshuffle()

