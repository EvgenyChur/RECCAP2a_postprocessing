# -*- coding: utf-8 -*-
"""
Task: Open NetCDF files with xarray module and check the results of interpolation
      Main parameter --> area of the reinterpolated pixels. Should be the same 

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-06-29 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-28 Evgenii Churiulin, MPI-BGC
           Updated script structure 
    1.3    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.4    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

#=============================     Import modules     =========================
# -- Standard:
import os
import sys
import numpy as np
import xarray as xr
import pandas as pd
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries import comp_area_lat_lon
#=============================   Personal functions   =========================

# onep_nc --> Open NetCDF file and add new field area to the data.
#             Area - is area of each pixel at the global scale
def open_nc(
        # input variables:
        data:str,             # Input path
        tdata:list[str],      # Time settings
        # Output variables:
    ) -> xr.Dataset:          # Dataset with data
    # -- Start processing:
    nc = (xr.open_dataset(data, decode_times = False)
            .assign_coords({'time' : pd.date_range(tdata[0], tdata[1], freq = "M")})
            .sel(time=slice(tdata[2],tdata[3]))
         )
    # -- Add area field:
    nc = nc.assign(xr.Dataset({'area': (('lat', 'lon'),
                      comp_area_lat_lon(nc.lat.values, nc.lon.values))}, 
                      coords = {'lat' : nc.lat.values, 'lon' : nc.lon.values}))
    return nc

# frac_info --> get actual burned area fractions:
def frac_info(ds1:xr.Dataset, ds2:xr.Dataset, var:str):
    return (ds1[var] * ds2.area).sum({'lat','lon'}).data[0]


if __name__ == '__main__':
    # =============================   User settings   ======================
    # Do you want to use cluster (True / False) ?
    lcluster = True
    # -- Input data:
    main = '../scratch/evchur/OCN/DATA4ctr_interpolation' if lcluster else 'C:/Users/evchur/Desktop/DATA/TESTS'
    # =============================    Main program   ======================
    exp_s21_1d  = main + '/selectedeu_s2.1_s2.2grid.nc'
    exp_S22_1d  = main + '/selectedeu_S2.2.nc'
    exp_s21_05d = main + '/selectedeu_S2.1_05deg.nc'
    # -- Time limits:
    time_set = ['1950-01-01', '2022-01-01', '1960', '2020']
    # -- Research parameter:
    var = 'burnedArea'
    # -- Experiment S2.1 - grid resolution 1.0 deg:
    s21_1d  = open_nc(exp_s21_1d , time_set)
    # -- Experiment S2.2 - grid resolution 1.0 deg:
    s22_1d  = open_nc(exp_S22_1d , time_set)
    # -- Experiment S2.1 - grid resolution 0.5 deg:
    s21_05d = open_nc(exp_s21_05d, time_set)
    # -- Print results:
    print('Original 0.5degree S2.1 = %i km2'    % frac_info(s21_05d, s22_1d, var))
    print('Original 0.5degree S2.2 = %i km2'    % frac_info(s22_1d , s22_1d, var))
    print('Remapped S2.1 to S2.2 grid = %i km2' % frac_info(s21_1d , s21_1d, var))
#=============================    End of program   ============================
