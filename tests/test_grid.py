# -*- coding: utf-8 -*-

from esa_cci_sm.grid import CCICellGrid, CCILandGrid
import unittest
import numpy as np

class GridTest(unittest.TestCase):

    def test_C3SCellGrid(self):
        grid = CCICellGrid()
        gp, dist = grid.find_nearest_gpi(75.625, 14.625)
        assert gp == 602942
        lon, lat = grid.gpi2lonlat(602942)
        assert lon == 75.625
        assert lat == 14.625
        assert np.where(grid.get_grid_points()[0] == 602942)[0][0] == 434462  # index
        assert grid.get_grid_points()[1][434462] == lon
        assert grid.get_grid_points()[2][434462] == lat
        assert grid.gpi2cell(602942) == 1856
        assert grid.gpis.size == 1036800
        assert grid.gpis[0] == 1035360
        assert np.unique(grid.get_grid_points()[3]).size == 2592


        lon, lat = grid.gpi2lonlat(642933)
        assert lon == -6.625
        assert lat == 21.625
        assert np.where(grid.get_grid_points()[0] == 642933)[0][0] == 393813  # index
        assert grid.get_grid_points()[1][393813] == lon
        assert grid.get_grid_points()[2][393813] == lat
        assert grid.gpi2cell(642933) == 1246



    def test_landgrid(self):
        grid = CCILandGrid()
        gp, dist = grid.find_nearest_gpi(75.625, 14.625)
        assert gp == 602942
        lon, lat = grid.gpi2lonlat(602942)
        assert lon == 75.625
        assert lat == 14.625
        assert np.where(grid.get_grid_points()[0] == 602942)[0][0] == 177048  # index
        assert grid.get_grid_points()[1][177048] == lon
        assert grid.get_grid_points()[2][177048] == lat
        assert grid.gpi2cell(602942) == 1856
        assert grid.gpis.size == 1036800
        assert grid.activegpis.size == 244243
        assert grid.gpis[0] == 1035360
        assert grid.activegpis[0] == 999942
        assert np.unique(grid.get_grid_points()[3]).size == 1001



if __name__ == '__main__':
    unittest.main()

