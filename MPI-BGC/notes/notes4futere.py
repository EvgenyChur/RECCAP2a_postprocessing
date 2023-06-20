# -*- coding: utf-8 -*-
"""
Task: Collection of notes for future plans, ideas or just nice examples

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-11-11 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     ===================
import os
import sys
import xarray as xr 
#import hvplot.xarray
from sklearn.metrics import mean_squared_error                                 # for the first example

sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.path_settings    import get_path_in
# =============================    Main program   =======================

"""
from sklearn.metrics import mean_squared_error
import xskillscore as xs



ocn21 = lst4data[0]['npp']
ocn22 = lst4data[1]['npp']


#rmse = mean_squared_error(ocn21, ocn22, squared = False)
rmse = xs.rmse(ocn21, ocn22, dim = 'time')

rmse.plot(robust= True, figsize = (10, 8), cmap="gist_earth_r")
"""

# 1. Calculations RMSE and MSE
y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]
mse = mean_squared_error( y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared = False)
print (f'mse: {mse}', f'rmse: {rmse}')


# 2. Test cycle while + input from keyboard
required_number = '18'
while True:
    number = input("Enter the number\n")
    if number == required_number:
        print ("GOT IT")
        break
    else:
        print ("Wrong number try again")
print('ha')

# 3. Basic options of xarray module
# Input path with ESA-CCI data
esa_pin, esa_param  = get_path_in(['BA_MODIS'], 'burned_area')

# 4.1 Open NetCDF
ds   = xr.open_dataset(esa_pin[0])
var  = 'burned_area'

# 4.2 Print common information about netcdf
print(ds, '\n')
ds.info()                            # look at nc representation
print('\n', ds.data_vars, '\n')      # look at nc variables
print('\n', ds.dims     , '\n')      # look at nc dimensions
print('\n', ds.coords   , '\n')      # look at nc coordinates
print('\n', ds.attrs    , '\n')      # look at nc attributes  

print(ds[var])         # parameter 
print(ds[var].coords)  # coordinates for parameter  
print(ds[var].attrs)   # specific attributes for parameter

# 4.3 Indexing and selecting data
'''
Selection by position (INDEX)
    1. selecting data by position using .isel() with values or slices
    2. selected data by coordinate label/values using .sel() with values or slices
    3. Use nearest-neigbor lookuo with .sel()
    4. Use interp() to interpolate by coordinates labels
'''
a = ds[var].data
print(a.shape)
print(a.ndim)
print(a[:, 50, 100])                                                           # Extract a timeseries for pixel
print('isel method test \n', ds[var].isel(), '\n')                             # no selection (all data)
print(ds[var].isel(lat = 100))                                                 # Select data for all timestep and longitude,
                                                                               # but only for latitude with index 100
print(ds[var].isel(lat = 100, time = [-2, -1]))                                # Select data for lat = 100 and timeslise (last 2)
print(ds[var].isel(lat = 100, time = slice(10, 20)))                           # Select data for lat = 100 and timeslise (10 to 20)

'''
Selection by label:
    a. A single coordinate label (time = '2021-03-01')
    b. A list or array coordinate labels
    c. Slice object with coordinates labels
'''
print(ds[var].sel(time = '2013'))                                              # select year
print(ds[var].sel(time = slice('2013-01-01','2014-12-31')).data)               # select period years  


# -- Selecting by nearest-neighbor lookups (point, area and area + time)
print(ds[var].sel(lat = 39.5, lon = 50.7, method = 'nearest'))
print(ds[var].sel(lat = slice(55, 45.5), lon = slice(51, 56.7)))
print(ds[var].isel(time = 0).sel(lat = slice(55, 45.5),lon = slice(51, 56.7)))
# -- Simple interpolation (doesn't work with area)
print(ds[var].interp(lat = [10, 12.2, 13.5], method='nearest'))

# 4.5 Visualization:
# 1D plot  (line)
(ds[var].sel(lon = 100, lat = 10, method = 'nearest')
        .plot(marker='o', size = 6))
# 2D plot  (map)
(ds[var].isel(time = -10).sel(lon = slice(20, 100), lat = slice(50, 20))
        .plot(robust = True, figsize = (8, 6)))
# 3D plot  (Faceting)
(ds[var].sel(time = slice("2010", "2011"))
        .plot(col = 'time', col_wrap=6, robust= True))

# Additional option for visualiztion:

# compare plots of temperature at three different latitudes
(ds[var].sel(lat = [-40, 0, 40], time = "2013", method = 'nearest')            # 1D for 3 lines (interesting option)  
        .plot(x = 'lon', hue = 'lat', figsize = (8,6)))

# colorbar
colorbar_kwargs = {'orientation' : 'horizontal'      ,
                   'label'       : 'my clustom label',
                   'pad'         : 0.2               }

(ds[var].isel(lon = 1)
        .plot(x = 'time', robust=True, cbar_kwargs = colorbar_kwargs))         # 2D plot with additional settings


#ds[var].hvplot()                                                               # Interactive visualization using hvplot (line)
#ds[var].isel(time = 1).hvplot()                                                # Interactive visualization using hvplot (2D)

# Histograms
ds[var].plot()
print('END program')
#=============================    End of program   ============================ 
