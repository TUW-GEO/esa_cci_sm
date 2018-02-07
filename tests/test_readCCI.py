
from hsaf_cci_042.interface import CCI_SM_v042_025Img
from hsaf_cci_042.reshuffle import main
from hsaf_cci_042.interface import CCITs

from os.path import join

file = 'ESACCI-SOILMOISTURE-L3S-SSMV-PASSIVE-20161229000000-fv04.2.nc'
year = '2016'
parameter = ['sm']

path_grid = '/home/fabio/Desktop/PyCharm_Workspace/HSAF/Product_Validation_Analysis/download/esa_cci'
path_ts = '/home/fabio/Desktop/PyCharm_Workspace/HSAF/Product_Validation_Analysis/download/esa_cci_ts'

date_from = '2016-12-27'
date_to = '2016-12-30'
var = 'sm'

# Get CCI image object
img = CCI_SM_v042_025Img(join(path_grid, year, file), parameter=parameter)

# Read CCI image object (with 0.25x0.25 grid)
image = img.read()
assert image.data['sm'].shape == (720, 1440)

#  CCI method to convert data from to ts
main([path_grid, path_ts, date_from, date_to, var])

# Test for reading ts from nc point file
ds = CCITs(path_ts)
ts = ds.read(45, 15)




