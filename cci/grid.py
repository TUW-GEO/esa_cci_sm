import numpy as np

from pygeogrids.grids import BasicGrid


def CCI025Cellgrid():
    """
    Class for the CCI Version 0.42 0.25deg cell grid.
    """

    resolution = 0.25

    lon, lat = np.meshgrid(
        np.arange(-180 + resolution/2, 180 + resolution/2, resolution),
        np.arange(-90 + resolution/2, 90 + resolution/2, resolution))

    return BasicGrid(lon.flatten(), lat.flatten()).to_cell_grid(cellsize=5.)