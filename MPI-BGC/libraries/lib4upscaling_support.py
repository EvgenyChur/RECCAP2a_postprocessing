# -*- coding: utf-8 -*-
__all__ = [
    'get_upscaling_ba_veg_class',
    'get_upscaling_ba',
]
"""
Module has functions for upscaling of burned area data:
    a. get_upscaling_ba_veg_class --> upscalling burned area PFT
    b. get_upscaling_ba --> upscaling total burned area data

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-09-15 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-11 Evgenii Churiulin, MPI-BGC
           Adapting script for cluster, add new enviroment settings
    1.3    2023-03-13 Evgenii Churiulin, MPI-BGC
           Adapting module settings
    1.4    2023-05-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================== Import modules ======================
# -- Standard modules:
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Optional
# -- Persnol modules:
from settings import get_path_in, get_output_path, logical_settings, config
from lib4visualization import create_fast_xarray_plot as xrplot
from lib4sys_support import makefolder
import lib4xarray as xrlib

# =============================== User functions ======================
def get_upscaling_ba_veg_class(
    # Input variables:
    dataset:xr.DataArray,            # Original ESA-CCI data (for example: BA_MODIS)
    var:str,                         # Research parameter
    lreport: Optional[bool] = False, # Do you want to get more information about input and output data?
    lplot: Optional[bool] = False,   # Do you want to create data for control plot?
    # OUTPUT variables:
    ) -> tuple [
        xr.DataArray,                # esa_ba -> Burned area over all PFT with 0.5 deg - resolution step
        pd.DataFrame,                # y_ba025 -> total burned area for grid (0.25 deg - resolution step)
        pd.DataFrame,                # y_baf025 -> total burned area fraction for grid (0.25 deg - resolution step)
        pd.DataFrame,                # y_ba05 -> total burned area for grid (0.5 deg - resolution step)
        pd.DataFrame,                # y_baf05 -> total burned area fraction for grid (0.5 deg - resolution step)
    ]:
    """ Take 0.25 grid and upscale it to 0.5 grid - parameter
    burned_area_by_vegetation class
    """
    # -- Local variables:
    ret_coef = 1e9
    res_step = 2    # (0.25 * 2) = 0.5 
    grid_step = 2

    # -- Get time steps
    time_steps = dataset.time

    tot_ba025  = [] # total burned area old
    tot_ba05   = [] # total burned area new 
    tot_baf025 = [] # total fraction (old)
    tot_baf05  = [] # total fraction (new)

    data_xr = []
    for tstep in range(len(time_steps)):
        # -- Get burned area data
        ba_old = dataset[var][tstep]
        # -- Get information about original data
        if lreport:
            print('SUM before', ba_old.data.sum())
        # -- Get coordinates
        latitude  = int(len(ba_old.lat) / res_step)
        longitude = int(len(ba_old.lon) / res_step)
        veg_class = int(len(ba_old.vegetation_class))
        # -- Create zero arrays for data
        ba_new = np.zeros((veg_class, latitude, longitude))
        lats   = np.zeros(latitude)
        lons   = np.zeros(longitude)
        pfts   = np.zeros(veg_class)
        # -- Create time index
        time = str(time_steps[tstep].data)
        dt   = pd.to_datetime(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000000000"))
        # Create new grid:
        for i in range(latitude):
            lats[i] = (ba_old.lat[i * grid_step] + ba_old.lat[i * grid_step + 1]) / grid_step
        
        for j in range(longitude):
            lons[j] = (ba_old.lon[j * grid_step] + ba_old.lon[j * grid_step + 1]) / grid_step

        for z in range(veg_class):
            pfts[z] = ba_old['vegetation_class'][z].data
        
        for z in range(veg_class):
            for i in range(latitude):
                for j in range(longitude):
                    ba_new[z, i, j] = (ba_old.data[z, i * grid_step    , j * grid_step    ] +
                                       ba_old.data[z, i * grid_step + 1, j * grid_step    ] +
                                       ba_old.data[z, i * grid_step    , j * grid_step + 1] +
                                       ba_old.data[z, i * grid_step + 1, j * grid_step + 1] )
        # -- Create dataarray:
        ba_array = xr.DataArray(ba_new, 
                                coords = {'vegetation_class': pfts, 'lat': lats,'lon': lons},
                                dims   = ["vegetation_class", "lat", "lon"])
        # -- Add time step:
        ba_array = ba_array.assign_coords(time = dt )
        ba_array = ba_array.expand_dims(dim = "time")
        # -- Add final data to the list over timesteps
        data_xr.append(ba_array)

        # -- Get info about new data:
        if lreport:
            print('SUM after', ba_new.sum(), '\n')

        # -- Prepare data for linear plot:
        if lplot:
            ba_frac025 = (dataset['burned_area_in_vegetation_class'][tstep] * ret_coef) / dataset['area']
            # -- Get new area for grid points
            ba_frac05 = (ba_array * ret_coef) / xrlib.comp_area_lat_lon(ba_array.lat.values,
                                                                        ba_array.lon.values)
            # -- Get total values over time steps (burned area and burned fraction)
            tot_ba025.append(
                pd.concat([pd.Series(dt), pd.Series(ba_old.data.sum())], axis = 1))
            tot_ba05.append(
                pd.concat([pd.Series(dt), pd.Series(ba_new.sum())     ], axis = 1))
            tot_baf025.append(
                pd.concat([pd.Series(dt), pd.Series(ba_frac025.data.sum())], axis = 1))
            tot_baf05.append(
                pd.concat([pd.Series(dt), pd.Series(ba_frac05.data.sum())] , axis = 1))

    # -- Get new dataset with 0.5 resolution grid (Burned area)
    esa_ba = xr.concat(data_xr, dim = 'time')
    if lplot:
        # Create time series over timestep (burned area and burned fraction)
        y_ba025  = pd.concat(tot_ba025 , axis = 0) # 0.25 grid step
        y_baf025 = pd.concat(tot_baf025, axis = 0) # 0.25 grid step
        y_ba05   = pd.concat(tot_ba05  , axis = 0) # 0.5 grid step
        y_baf05  = pd.concat(tot_baf05 , axis = 0) # 0.5 grid step 
        return esa_ba, y_ba025, y_baf025, y_ba05, y_baf05
    else:
        return esa_ba

# 2.2: Function --> get_upscaling_ba
def get_upscaling_ba(
        # Input variables:
        dataset:xr.DataArray,                    # Original ESA-CCI data (for example: BA_MODIS).
        var:str,                                 # Research parameter
        lreport: Optional[bool] = False,         # Do you want to print total values over timesteps?
        # OUTPUT variables:
        ) -> xr.DataArray:                       # Burned area over all PFT with 0.5 deg - resolution step.

    # -- Local variables:
    res_step = 2    # (0.25 * 2) = 0.5 
    grid_step = 2
    # -- Get time steps:
    time_steps = dataset.time
    data_xr = []
    for tstep in range(len(time_steps)):
        # -- Get burned area data
        ba_old = dataset[var][tstep]
        latitude  = int(len(ba_old.lat) / res_step)
        longitude = int(len(ba_old.lon) / res_step)
        # -- Get info about initial data
        if lreport == True:
            print('SUM before'  , ba_old.data.sum())
        # -- Create zero arrays for data
        ba_new = np.zeros((latitude, longitude))
        lats   = np.zeros(latitude)
        lons   = np.zeros(longitude)
        # Create time index
        time = str(time_steps[tstep].data)
        dt   = pd.to_datetime(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000000000"))
        # Create new grid  (latitude, longitude, burned area)
        for i in range(latitude):
            lats[i] = (ba_old.lat[i * grid_step] + ba_old.lat[i * grid_step + 1]) / grid_step
        for j in range(longitude):
            lons[j] = (ba_old.lon[j * grid_step] + ba_old.lon[j * grid_step + 1]) / grid_step
        for i in range(latitude):
            for j in range(longitude):
                ba_new[i, j] =(ba_old.data[i * grid_step    , j * grid_step    ] +
                               ba_old.data[i * grid_step + 1, j * grid_step    ] +
                               ba_old.data[i * grid_step    , j * grid_step + 1] +
                               ba_old.data[i * grid_step + 1, j * grid_step + 1] )
        # -- Get info about new data:
        if lreport == True:
            print('SUM after', ba_new.sum(), '\n')
        # -- Create new dataarray:
        ba_array = xr.DataArray(ba_new, coords = {'lat': lats,'lon': lons}, 
                                        dims   = ["lat", "lon"])

        ba_array = ba_array.assign_coords(time = dt )
        ba_array = ba_array.expand_dims(dim = "time")
        data_xr.append(ba_array)
    # -- Get new dataset with 0.5 resolution grid
    esa_ba = xr.concat(data_xr, dim = 'time')
    return esa_ba

if __name__ == '__main__':
    # ============================= Users settings =======================
    # -- Logical parameteres:
    # -- Define logical settings (lcluster, lnc_info,station_mode, lvis_lines, lBasemap_moment:
    lsets = logical_settings(lcluster = True)
    # -- Other logical parameters
    linfo = lsets.get('lnc_info') # Get more info about NetCDF
    lplot = True                  # Do you want to get plots for burned area (only):
    lresmp = False                # Do you need resample (monthly to annual)?
    lreport = True                # Do you need detailed report about upscalling?

    # -- Get basic user settings for datasets (NDEP, MODIS datasets)
    bcc = config.Bulder_config_class()
    tlm = bcc.user_settings()

    # -- Select actual dataset parameters
    name4ndep = 'NDEP'
    name4modis = 'MODIS'
    ndep_datasets = [name4ndep]
    esa_datasets  = [name4modis]

    # -- Select research parameter (3D or 4D fields):
    lparam = 'burned_area'
    #lparam = 'burned_area_in_vegetation_class'

    # -- Define input (NDEP, ESA MODIS) and output paths and create folder for results
    ndep_pin, ndep_param = get_path_in(ndep_datasets, 'ndep', lsets)
    esa_pin, esa_param = get_path_in([f'BA_{name4modis}'] , 'burned_area', lsets)
    data_OUT = makefolder(get_output_path(lsets).get('lib4upscaling_support'))
    print(f'Your data will be saved at {data_OUT}')

    # -- Settings for 2D maps:
    plt_settings = {
        'orig_grid' : {
            'robust'   : True,
            'colormap' : 'hot_r',
            'vmin'     : 0.0,
            'vmax'     : 0.2,
            'col'      : None,
            'col_wrap' : None,
            'title'    : 'Burned area ',
            'output'   : data_OUT + 'ORIG_grid_720-1440.png',
        },
        'new_grid' : {
            'robust'   : True,
            'colormap' : 'hot_r',
            'vmin'     : 0.0,
            'vmax'     : 0.2,
            'col'      : None,
            'col_wrap' : None,
            'title'    : 'Burned area ',
            'output'   : data_OUT + 'NEW_grid_360-720.png',
        },
        'ndep_grid' : {
            'robust'   : True,
            'colormap' : 'hot_r',
            'vmin'     : 0.0,
            'vmax'     : 0.2,
            'col'      : None,
            'col_wrap' : None,
            'title'    : 'Burned area ',
            'output'   : data_OUT + 'NDEP_grid_360-720.png',
        },
    }

    # ==============================  Main program  =====================
    print('START program')
    # -- Read data (NDEP, ESA-CCI MODIS)
    print(ndep_pin)
    ndep_data = xrlib.get_data(
        ndep_pin, ndep_datasets, name4ndep, ndep_datasets,tlm, linfo = linfo, lresmp = lresmp)[0]
    esa_data  = xrlib.get_data(
        esa_pin , esa_datasets , 'burned_area', [lparam], tlm, linfo = linfo, lresmp = lresmp)[0]

    # -- Start upscaling (two different algorithms for burned area and
    #                  burned_area_in_vegetation_class)
    if lparam == 'burned_area_in_vegetation_class':
        esa_ba, old_ba, old_frac, new_ba, new_frac = get_upscaling_ba_veg_class(
            esa_data, lparam, lreport = lreport, lplot = lplot)
    else:
        esa_ba = get_upscaling_ba(esa_data, lparam, lreport = lreport)

    # -- Reinterpolation to NDEP grid (size is the same):
    ba_frac = esa_ba.interp_like(ndep_data.drop_dims('time'), method = 'nearest')
    # -- Create burned area simple plots for output results:
    if lplot and lparam == 'burned_area':
        # Satellite dataset original grid (1440 * 720):
        xrplot(esa_data['burned_area'][0] *4, 'orig_grid', plt_settings)
        # Satellite dataset OCN grid (720 - 300)
        xrplot( esa_ba[0], 'new_grid', plt_settings)
        # Satellite dataset NDEP grid (720 - 300) --> New grid at NDEP coordinates
        xrplot(ba_frac[0], 'ndep_grid', plt_settings)
    print('END program')

# =============================== Program END  ============================
