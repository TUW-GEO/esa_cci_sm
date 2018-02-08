from hsaf_cci_042.grid import CCI025Cellgrid

def test_CCI025_cell_grid():
    hsaf_grid = CCI025Cellgrid()
    assert hsaf_grid.activegpis.size == 1036800
    assert hsaf_grid.activegpis[153426] == 153426
    assert hsaf_grid.activearrcell[153426] == 1409
    assert hsaf_grid.activearrlat[153426] == -63.375
    assert hsaf_grid.activearrlon[153426] == 16.625



if __name__ == '__main__':
    test_CCI025_cell_grid()