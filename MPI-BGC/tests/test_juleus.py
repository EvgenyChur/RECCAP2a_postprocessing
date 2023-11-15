# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy  as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def comp_area_lat_lon(lat, lon):
    '''
    Task : Create mesh grid for actual coordinates
    
    Author: Ana Bastos

    Parameters
    ----------
    lat, lon : FLOAT
        Latitude and Longitude arrays from NetCDF files.

    Returns
    -------
    area : 2D array.
    '''
    radius = 6.37122e6 # in meters
 
    lat  = np.squeeze(lat); lon = np.squeeze(lon)
    nlat = len(lat)
    nlon = len(lon)
    
    # LATITUDE
    lat_edge         = np.zeros((nlat + 1))
    lat_edge[0]      = max(-90, lat[0] - 0.5 * (lat[1] - lat[0])); #ana
    lat_edge[1:nlat] = 0.5 * (lat[0:nlat-1] + lat[1:nlat])
    lat_edge[nlat]   = min(90, lat[nlat - 1] - 0.5 * (lat[nlat - 2] - lat[nlat - 1]))
    dlat             = np.diff(lat_edge)
    
    #LONGITUDE
    lon_edge         = np.zeros((nlon + 1))
    lon_edge[0]      = lon[0] - 0.5 * (lon[1] - lon[0])
    lon_edge[1:nlon] = 0.5 * (lon[0:nlon-1] + lon[1:nlon])
    lon_edge[nlon]   = lon[nlon - 1] - 0.5 * (lon[nlon - 2] - lon[nlon - 1])
    dlon             = np.diff(lon_edge)
    
    dlon_2d, dlat_2d = np.meshgrid(dlon, dlat) # create mesh with cell size in deg    
    lon_2d , lat_2d  = np.meshgrid( lon,  lat)

    dy = radius * (dlat_2d * (np.pi / 180.0))
    dx = radius * np.multiply(dlon_2d * (np.pi / 180.0), np.cos(lat_2d * (np.pi / 180.0)))

    area = np.multiply(dx, dy)
    if np.sum(area) < 0:
        area = -1 * area

    return area

#jul_1d   = 'C:/Users/evchur/Desktop/JULES_S2Prog_burntArea_1deg.nc'
#jul_05d  = 'C:/Users/evchur/Desktop/JULES_S2Prog_burntArea_05deg.nc'
jul_or   = '../scratch/evchur/JULES/Prog/4test/JULES_S2_v6.3_cVeg.nc'
jul_1d   = '../scratch/evchur/JULES/Prog/4test/JULES_S2Prog_cVeg_1deg.nc'

#jul_or   = 'X:/scratch/evchur/JULES/Prog/4test/JULES_S2_v6.3_cVeg.nc'
#jul_1d   = 'X:/scratch/evchur/JULES/Prog/4test/JULES_S2Prog_cVeg_1deg.nc'
#jul_05d  = 'C:/Users/evchur/Desktop/JULES_S2Prog_cVeg_05deg.nc'

#"X:\scratch\evchur\JULES\Prog\4test\JULES_S2Prog_cVeg_1deg.nc"

ocn_05d = 'C:/Users/evchur/Desktop/DATA/OCN_fire/RECCAP2_DATA\OCN_S0_cVeg.nc'

#grid4domain[i] = grid4domain[i].interp_like(
#    inter2grid.drop_dims('time'), method = 'nearest' ) 


#j1 = 'C:/Users/evchur/Desktop/JULES_S2Prog_cVeg.nc'
#j2 = 'C:/Users/evchur/Desktop/JULES_S2Diag_cVeg_1deg.nc'

# = 1e-9

param = 'cVeg'

nc_jul = xr.open_dataset(jul_or)
#nc_ocn = (
#    xr.open_dataset(ocn_05d, decode_times = False)
#      .assign_coords({'time': pd.date_range('1950-01-01', '2021-01-01', freq = '1M')})
#)

vo = nc_jul[param][0].plot( cmap = 'hot_r', vmin = 0)
vs1 = nc_jul[param]
#plt.close(fig)      
plt.show()
plt.savefig('JUL_orig.png', format='png', dpi = 300) 

plt.gcf().clear()

nc_jul2 = xr.open_dataset(jul_1d)
vs2 = nc_jul2[param]
vn = nc_jul2[param][0].plot( cmap = 'hot_r', vmin = 0)
plt.show()
plt.savefig('JUL_05d.png', format='png', dpi = 300) 
plt.gcf().clear()
 

"""

def get_data(path, param, repl = False):
    
    rec_coef    = 1e-9        # m2 to 1000 km2
    
    nc = xr.open_dataset(path)
    
    # -- Rename attributes
    if repl == True:
        nc = nc.rename({'longitude':'lon', 'latitude':'lat'})
    
    nc = nc.assign(xr.Dataset({'area': (('lat', 'lon'),
                  comp_area_lat_lon(nc.lat.values, nc.lon.values))},
                  coords = {'lat' : nc.lat.values, 'lon' : nc.lon.values}))

    if param in ('gpp', 'npp', 'fFire', 'nbp'):
        # Convert kg C m-2 s-1  to gC m-2 yr-1
        nc[param] = (nc[param] * 1000 * 24  * 3600 * 
                     nc[param].time.dt.days_in_month)
    elif param == 'burned_area':
        nc['burned_area'] = ((nc[param] / 100) * nc['area'] * rec_coef)
        
    return nc

#nc_05d  = get_data(jul_05d, param)
print(1)
nc_1d   = get_data(jul_1d , param, repl = False)
print(2)
nc_orig = get_data(jul_or , param, repl = True) 


def means(nc, var):
    return nc[var].sum(dim = {'lat', 'lon'}).groupby('time.year').mean() 

#ba_05d  = means(nc_05d , param) 
ba_1d   = means(nc_1d  , param) 
ba_org  = means(nc_orig, param) 

# -- Plot
fig = plt.figure(figsize = (12,7))
ax  = fig.add_subplot(111) 

ax.plot(  ba_1d.year, ba_1d  , label = '1', linestyle = '--' )
#ax.plot( ba_05d.year, ba_05d , label = '2' )
ax.plot( ba_org.year, ba_org , label = '3', linestyle = ':' )

#ax.plot( b2.year, b2 , label = '5' )
ax.legend()

plt.savefig('LINE_PLOT.png', format='png', dpi = 300) 
"""