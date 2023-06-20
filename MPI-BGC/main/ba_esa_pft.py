# -*- coding: utf-8 -*-
"""
Script for visualization of statistical metrics such as mean, std and trend for
ESA-SSI MODISv5.1 data. Actual research parameter burned_area_in_vegetation_class.

Information for LandCover Class Table is located at
# https://developers.google.com/earth-engine/datasets/catalog/ESA_CCI_FireCCI_5_1#bands

Important information: 
    For the first run you have to adapt new parameters:
        1. Select option for sys.path.append (comment or not, if not select your data)
        2. Select region 

P.S.: If you run this script from PuTTY with Windows you can get the error:
      PuTTY X11 proxy: unable to connect to forwarded X server: --> to fix it you 
      have to install Xming and run it first.

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-06-10 Evgenii Churiulin, MPI-BGI
           Initial release
    1.2    2022-07-26 Evgenii Churiulin, MPI-BGI
           Adapted for more modern version of other scripts and cluster work 
    1.3    2022-10-28 Evgenii Churiulin, MPI-BGI
           Updated functions for new versions of scripts from xrlib
    1.4    2022-11-14 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.5    2023-05-15 Evgenii Churiulin, MPI-BGC
           Code refactoring + transfered get_figure4lcc function to vis_controls module
"""

# =============================     Import modules     ===================
# 1.1: Standard modules
import os
import sys
import numpy as np
import xarray as xr

# 1.2 Personal module
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4pft import modis_pft
from libraries.lib4sys_support import makefolder
from libraries.lib4xarray import get_data
from calc.vis_controls import get_figure4lcc
from settings.path_settings import get_path_in, output_path

# =============================   Personal functions   ==================
# 2.1: get_title_path --> Get actual plot subtitle for each ESA-CCI PFT
def  get_title_path(
        # Input variables:
        veg_classes:list[dict],          # Settings for ESA-CCI PFT
        numb:list[int],                  # Actual index of each ESA-CCI PFT
        # OUTPUT variables:
    ) -> list[str]:                      # Plot subtitles for each ESA-CCI PFT
    # -- Get subtitle for each PFT
    title    = []  # Output titles
    for vclass in veg_classes:
        if vclass['index'] in (numb):
            title.append(vclass['veg_class'])
    return title

# 2.2: get_mean_std --> Get annual MEAN and STD values for each grid points:
def get_mean_std(
        # Input variables:
        ds:xr.DataArray,                 # Research dataset
        veg_classes:list[dict],          # Settings for ESA-CCI PFT
        numb:list[int],                  # Actual index of each ESA-CCI PFT
        # OUTPUT variables:
    ) -> tuple[
            list[xr.DataArray],      # MEAN values of each ESA-CCI PFT
            list[xr.DataArray],      # STD values of each ESA-CCI PFT
    ]:
    # -- Get statistical data (MEAN and STD)
    lst4mean = []
    lst4std  = []
    for vclass in veg_classes:
        if vclass['index'] in (numb):
            lst4mean.append(ds[:, vclass['index'], :, :].mean('time'))
            lst4std.append( ds[:, vclass['index'], :, :].std('time' ))
    return  lst4mean, lst4std 

# 2.3: get_trend --> Get annual time trend for each grid points
def get_trend(
        # Input variables:
        ds:xr.DataArray,                 # Research dataset
        veg_classes:list[dict],          # Settings for ESA-CCI PFT
        numb:list[int],                  # Actual index of each ESA-CCI PFT
        # OUTPUT variables:
    ) -> list[xr.DataArray]:             # Time trend values of each ESA-CCI PFT
    # -- Get  data for TIME TRENDS calculations:
    lst4trends = []
    for vclass in veg_classes:
        if vclass['index'] in (numb):
            # Get data
            data4trend = ds[:, vclass['index'], :, :].values
            year4trend = ds[:, vclass['index'], :, :].time.dt.year.values
            # Reshape to an array with as many rows as years and as
            # many columns as there are pixels
            val = data4trend.reshape(len(year4trend), -1)
            # Do a first-degree polyfit
            regressions = np.polyfit(year4trend, val, 1)
            # Get the coefficients back
            trends = regressions[0,:].reshape(data4trend.shape[1],
                                              data4trend.shape[2])
            trends = xr.DataArray(trends, name = 'trends')
            lst4trends.append(trends)
    return lst4trends

# ================   User settings (have to be adapted)  ==================

# -- Logical parameters:
# Do you want to get more information about data?
linfo = False
# Activate algorithm for mean visualization?
lmean_plot = True
# Activate algorithm for std visualization?
lstd_plot = True
# Activate algorithm for trends visualization?
ltrend_plot = True

# -- Main settings:
# Research dataset: (ESA-CCI MODISv5.0):
datasets = ['BA_MODIS']
# Research domain (Global, Europe, Tropics, NH, Other):
region   = 'Global'
# Research parameter:
var      = 'burned_area'
# NetCDF attribute research parameter (burned_area_in_vegetation_class):
params   = ['burned_area_in_vegetation_class']

# -- Plot settings:
# Rows and columns numbers for collage plot (nrows*ncols):
nrows = 3
ncols = 3
# Plot titles:
nplt_mean  = 'Burned area annual MEAN for different PFT'
nplt_std   = 'Burned area annual STD for different PFT'
nplt_trend = 'Burned area TREND for different PFT'
# Settings for subplots (limits and colormap): Option 1 - Visible changes data
clb_lim1 = [
    {'mode':'burned_area', 'param':'mean' , 'ymin':  0.0 , 'ymax':   0.04  , 'cbar' : 'hot_r' },
    {'mode':'burned_area', 'param':'std'  , 'ymin':  0.0 , 'ymax':   0.02  , 'cbar' : 'hot_r' },
    {'mode':'burned_area', 'param':'trend', 'ymin': -1e-4, 'ymax':   1e-4  , 'cbar' : 'RdBu_r'},
]
# Settings for subplots (limits and colormap): Option 2 - Lower values for burned area
clb_lim2 = [
    {'mode':'burned_area', 'param':'mean' , 'ymin':  0.0 , 'ymax':   0.004 , 'cbar' : 'hot_r' },
    {'mode':'burned_area', 'param':'std'  , 'ymin':  0.0 , 'ymax':   0.002 , 'cbar' : 'hot_r' },
    {'mode':'burned_area', 'param':'trend', 'ymin': -1e-5, 'ymax':   1e-5  , 'cbar' : 'RdBu_r'},
]

# -- Select PFT groups and get actual PFT names for each PFT:
# Visible changes:
lst1 = [0, 2, 3, 4, 5, 10, 11, 12, 14]
# Small changes:
lst2 = [1, 6, 7, 8, 9, 13, 15, 16, 17]
vis_title   = get_title_path(modis_pft, lst1)
invis_title = get_title_path(modis_pft, lst2)

# =============================    Main program   ========================
if __name__ == '__main__':
    print('START program')
    # -- Define input and output paths and create folder for results:
    ipaths, ip_par = get_path_in(datasets, var)
    data_OUT = makefolder(output_path().get('ba_esa_pft'))
    print(f'Your data will be saved at {data_OUT}')
    # -- OUTPUT names for figures:
    pout = [# Group 1: PFT with visible changes in burned area (vis)
            data_OUT + f'{region}_MEAN4BA_vis.png'   ,
            data_OUT + f'{region}_STD4BA_vis.png'    ,
            data_OUT + f'{region}_TREND4BA_vis.png'  ,
            # Group 2: PFT with invisible or small changes in burned area (invis)
            data_OUT + f'{region}_MEAN4BA_invis.png' ,
            data_OUT + f'{region}_STD4BA_invis.png'  ,
            data_OUT + f'{region}_TREND4BA_invis.png']

    # -- Get initial data from NetCDF:
    lst4data = get_data(ipaths, datasets, var, params, linfo = linfo)[0]
    # -- Select your parameter and get results:
    data = lst4data[params[0]]  # act data
    lat  = data.lat.values      # latitude values
    lon  = data.lon.values      # longitude values
    # -- Get mean, std and time trends values for each PFT:
    vis_lst4mean  ,   vis_lst4std = get_mean_std(data, modis_pft, lst1)
    vis_lst4trend                 = get_trend(   data, modis_pft, lst1)

    invis_lst4mean, invis_lst4std = get_mean_std(data, modis_pft, lst2)
    invis_lst4trend               = get_trend(   data, modis_pft, lst2)

    # -- Start visualization:
    # a. Plot: MEAN values
    if lmean_plot  == True:
        print('Working on collages for MEAN values \n')
        # Plot 1
        get_figure4lcc(
            nrows, ncols, lon, lat, vis_lst4mean, var, 'mean', clb_lim1, region,
            vis_title, nplt_mean, pout[0],
        )
        # Plot 2
        get_figure4lcc(
            nrows, ncols, lon, lat, invis_lst4mean, var, 'mean', clb_lim2, region,
            invis_title, nplt_mean, pout[3],
        )
    # b. Plot: STD values
    if lstd_plot   == True:
        print('Working on collages for STD values \n')
        # Plot 3
        get_figure4lcc(
            nrows, ncols, lon, lat, vis_lst4std, var, 'std', clb_lim1, region,
            vis_title, nplt_std, pout[1],
        )
        # Plot 4
        get_figure4lcc(
            nrows, ncols, lon, lat, invis_lst4std, var, 'std', clb_lim2, region,
            invis_title, nplt_std, pout[4],
        )
    #  c. Plot: Trend
    if ltrend_plot == True:
        print('Working on collages for TREND values \n')
        # Plot 5
        get_figure4lcc(
            nrows, ncols, lon, lat, vis_lst4trend, var, 'trend', clb_lim1, region,
            vis_title, nplt_trend, pout[2],
        )
        # Plot 6
        get_figure4lcc(
            nrows, ncols, lon, lat, invis_lst4trend, var, 'trend', clb_lim2, region,
            invis_title, nplt_trend, pout[5],
        )
    print('END program')
# =============================    End of program   ======================
