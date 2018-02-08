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
                              "hsaf_cci_042_data", "esa_cci")
        startdate = "2016-12-27T00:00"
        enddate = "2016-12-31T00:00"
        parameters = ["SoilMoi0_10cm_inst", "SoilMoi10_40cm_inst"]
        ts_path = tempfile.mkdtemp()
        args = [inpath, ts_path, startdate, enddate] + parameters
        main(args)

        self.assertEquals(len(glob.glob(os.path.join(ts_path, "*.nc"))), 2593)

        ds = CCITs(ts_path)
        ts = ds.read(45, 15)
        ts_SM0_10_values_should = np.array([9.595, 9.593, 9.578,
                                            9.562, 9.555, 9.555, 9.556],
                                           dtype=np.float32)
        print ts['SoilMoi0_10cm_inst'].values
        # nptest.assert_allclose(ts['SoilMoi0_10cm_inst'].values,
        #                        ts_SM0_10_values_should, rtol=1e-5)
        # ts_SM10_40_values_should = np.array([50.065, 50.064, 50.062,
        #                                      50.060, 50.059, 50.059,
        #                                      50.059], dtype=np.float32)
        # nptest.assert_allclose(ts['SoilMoi10_40cm_inst'].values,
        #                        ts_SM10_40_values_should, rtol=1e-5)


if __name__ == '__main__':
    unittest.main()

