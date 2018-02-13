import os
import glob
import tempfile
import numpy as np
import numpy.testing as nptest
import unittest

from hsaf_cci_042.reshuffle import main
from hsaf_cci_042.interface import CCITs

class ReshuffleTest(unittest.TestCase):

    def test_reshuffle(self):
        inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "hsaf_cci_042_data", "esa_cci_sm_dailyImages", "passive")
        startdate = "2016-06-06T00:00"
        enddate = "2016-06-07T00:00"
        parameters = ["sm"]
        ts_path = tempfile.mkdtemp()
        args = [inpath, ts_path, startdate, enddate] + parameters
        main(args)

        self.assertEquals(len(glob.glob(os.path.join(ts_path, "*.nc"))), 2593)

        ds = CCITs(ts_path)
        ts = ds.read(45, 15)
        ts_values_should = np.array([1.29999995e-01, 9.99900000e+03],
                                    dtype=np.float32)
        nptest.assert_allclose(ts['sm'].values,
                               ts_values_should, rtol=1e-5)



if __name__ == '__main__':
    unittest.main()

