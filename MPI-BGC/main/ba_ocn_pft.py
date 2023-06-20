# -*- coding: utf-8 -*-
"""
Script for visualization of statistical metrics such as mean, std and trend for
OCN data. Actual research parameter burnedArea.

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-11-01 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-15 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.3    2023-05-15 Evgenii Churiulin, MPI-BGC
           Code rafactoring + transfered get_figure4lcc function to vis_controls module
"""

# =============================     Import modules     ===================
# 1.1: Standard modules
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr

# 1.2 Personal module
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4pft import ocn_pft
from libraries.lib4sys_support import makefolder
from libraries.lib4xarray import comp_area_lat_lon
from calc.vis_controls import get_figure4lcc
from settings.path_settings import get_path_in, output_path
# =============================   Personal functions   ===================

# ================   User settings (have to be adapted)  =================
# -- Logical parameters:
# Activate algorithm for visualization?
lplot = True

# -- Main settings:
# Research dataset: (OCN):
datasets = ['OCN_S2Diag']
# Research domain (Global, Europe, Tropics, NH, Other):
region = 'Global'
# Research parameter:
var = 'burnedArea'
# First year:
tstart = '2000-01-01'
# Last year:
tstop = '2021-01-01'
# Time step:
tstep = '1M'
# Recalculation coefficient (BA: m2 to 1000 km2):
rec_coef = 1e-9

# -- Plot settings:
# Rows and columns numbers for collage plot (nrows*ncols):
nrows = 3
ncols = 4
# Plot titles:
nplt_mean  = 'Burned area annual MEAN for different OCN PFT'
nplt_std   = 'Burned area annual STD for different OCN PFT'
nplt_trend = 'Burned area TREND for different OCN PFT'
# Settings for subplots (limits and colormap):
clb_lim = [
    {'mode' : var, 'param': 'mean' , 'ymin' :  0.0 , 'ymax' : 0.04, 'cbar' : 'hot_r' },
    {'mode' : var, 'param': 'std'  , 'ymin' :  0.0 , 'ymax' : 0.02, 'cbar' : 'hot_r' },
    {'mode' : var, 'param': 'trend', 'ymin' : -1e-4, 'ymax' : 1e-4, 'cbar' : 'RdBu_r'},
]

# -- Get actual PFT names for each PFT:
title = []
for vclass in ocn_pft:
    title.append(vclass['PFT'])

# =============================    Main program   =========================
if __name__ == '__main__':
    print('START program')
    # Important information:  pin_param - has None values in this script. Due to there
    #                         is no key attribute from attribute_catalog  of mclister.py
    #                         or mlocal.py modules. Nevertheless, you use this function
    #                         because of input path has correct name and pin_param is
    #                         unused in this script!

    # -- Define INPUT and OUTPUT paths with OCN model results and create OUTPUT folder:
    pin, pin_param = get_path_in(datasets, 'firepft')
    print(pin)
    data_OUT = makefolder(output_path().get('ba_ocn_pft'))

    print(f'Your data will be saved at {data_OUT}')
    # -- OUTPUT figures names:
    pout = [
        data_OUT + f'{region}_MEAN4BA_vis.png',
        data_OUT + f'{region}_STD4BA_vis.png',
        data_OUT + f'{region}_TREND4BA_vis.png',
        data_OUT + f'{region}_MEAN4PFT_ts.png',
    ]
    # -- Read-in NetCDF and get data in appropriate view:
    nc = (xr.open_dataset(pin[0], decode_times = False)
            .assign_coords({'time': pd.date_range(tstart, tstop, freq = tstep)}))
    # -- Add new field with area values:
    nc = nc.assign(xr.Dataset({'area': (('lat', 'lon'),
                      comp_area_lat_lon(nc.lat.values,
                                        nc.lon.values))},
                      coords = {'lat' : nc.lat.values,
                                'lon' : nc.lon.values}))
    # -- Convert units:
    nc[var] = nc[var] * nc['area'] * rec_coef * nc[var].time.dt.days_in_month
    nc = nc.resample(time = 'A').sum('time')
    # -- Select your parameter and get data for (parameter, latitude, longitude):
    ba_pft = nc[var]
    lat = ba_pft.lat.values
    lon = ba_pft.lon.values
    # -- Get annual mean, std and time trend values for each grid points (over time):
    lst4mean  = []
    lst4std   = []
    lst4trend = []
    for vclass in ocn_pft:
        # -- Calculating MEAN values:
        lst4mean.append(ba_pft[:, vclass['index'], :, :].mean('time'))
        # -- Calculating STD values:
        lst4std.append(ba_pft[ :, vclass['index'], :, :].std('time' ))
        # -- Calculating TREND values:
        data4trend = ba_pft[:, vclass['index'], :, :].values
        year4trend = ba_pft[:, vclass['index'], :, :].time.dt.year.values
        # Reshape to an array with as many rows as years and as many columns as there are pixels:
        val = data4trend.reshape(len(year4trend), -1)
        # Do a first-degree polyfit
        regressions = np.polyfit(year4trend, val, 1)
        # Get the coefficients back
        trends = regressions[0,:].reshape(data4trend.shape[1], data4trend.shape[2])
        trends = xr.DataArray(trends, name = 'trends')
        lst4trend.append(trends)

    # -- Visualization:
    if lplot  == True:
        # Plot 1 --> 'Working on collages for MEAN values'
        get_figure4lcc(
            nrows, ncols, lon, lat, lst4mean[1:], var, 'mean', clb_lim, region,
            title[1:], nplt_mean, pout[0],
        )
        # Plot 2 --> 'Working on collages for STD values \n'
        get_figure4lcc(
            nrows, ncols, lon, lat, lst4std[1:], var, 'std', clb_lim, region,
            title[1:], nplt_std  , pout[1],
        )
        # Plot 3--> 'Working on collages for TREND values \n'
        get_figure4lcc(
            nrows, ncols, lon, lat, lst4trend[1:], var, 'trend', clb_lim, region,
            title[1:], nplt_trend, pout[2],
        )
    print('END program')

# =============================    End of program   ======================
