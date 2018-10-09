from esa_cci_sm.grid import CCI025Cellgrid

def test_CCI025_cell_grid():
    """
    test for the grid function
    """
    ccigrid = CCI025Cellgrid()
    assert ccigrid.activegpis.size == 1036800
    assert ccigrid.activegpis[153426] == 153426
    assert ccigrid.activearrcell[153426] == 1409
    assert ccigrid.activearrlat[153426] == -63.375
    assert ccigrid.activearrlon[153426] == 16.625



if __name__ == '__main__':
    test_CCI025_cell_grid()