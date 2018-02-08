from hsaf_cci_042.grid import CCI025Cellgrid
import unittest

class GridTest(unittest.TestCase):

    def test_CCI025_cell_grid(self):
        hsaf_grid = CCI025Cellgrid()
        self.assertEquals(hsaf_grid.activegpis.size, 1036800)
        self.assertEquals(hsaf_grid.activegpis[153426], 153426)
        self.assertEquals(hsaf_grid.activearrcell[153426], 1409)
        self.assertEquals(hsaf_grid.activearrlat[153426], -63.375)
        self.assertEquals(hsaf_grid.activearrlon[153426], 16.625)

if __name__ == '__main__':
    unittest.main()


