# -*- coding: utf-8 -*-

from smecv_grid.grid import SMECV_Grid_v042

def CCICellGrid():
    return SMECV_Grid_v042(None)

def CCILandGrid():
    return SMECV_Grid_v042('land')