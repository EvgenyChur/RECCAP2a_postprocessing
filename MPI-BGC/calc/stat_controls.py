# -*- coding: utf-8 -*-
"""
Task: Realization of statistical algorithms for evaluation of OCN results

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-07-7 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.3    2023-05-04 Evgenii Churiulin, MPI-BGC
           Small changes related to code refactoring
"""
# =============================     Import modules     ====================
# 1.1: Standard modules
import os
import sys
import numpy as np
import xarray as xr
from typing import Optional
# =============================   Personal functions   ====================

# timmean --> Get actual data for MEAN calculations (for each grid point)
def timmean(
        # Input variables:
        lst4dts:list[str],                   # Names of datasets
        lst4data:list[xr.DataArray],         # Research datasets at the same order as **lst4dts**
        var:str,                             # Research parameter.
        fire_xarray: Optional[bool] = True,  # Are you working with fire_xarray.py script?
        fire_ratio: Optional[bool] = False,  # Are you working with fire_ratio.py script?
        # OUTPUT variables:
    ) -> list[xr.Dataset]:                               # Mean values for the research datasets.
    # Start computations:
    lst4mean = []
    for i in range(len(lst4dts)):
        if fire_xarray is True:
            lst4mean.append(lst4data[i][var].mean(['time']))
        elif fire_ratio is True:
            lst4mean.append(lst4data[i].mean(['time']))
    return lst4mean

# timstd --> Get actual data for STD calculations (for each grid point).
def timstd(
        # Input variables:
        lst4dts:list[str],                   # Names of datasets
        lst4data:list[xr.DataArray],         # Research datasets at the same order as **lst4dts**
        var:str,                             # Research parameter.
        fire_xarray: Optional[bool] = True,  # Are you working with fire_xarray.py script?
        fire_ratio: Optional[bool] = False,  # Are you working with fire_ratio.py script?
        # OUTPUT variables:
    ) -> list[xr.Dataset]:                   # STD values for each dataset
    # Start computations:
    lst4std  = []
    for i in range(len(lst4dts)):
        if fire_xarray == True:
            lst4std.append(lst4data[i][var].std(['time']))
        elif fire_ratio == True:
            lst4std.append(lst4data[i].std(['time']))
    return lst4std

# timtrend --> Trend values for research datasets (for each grid point).
def timtrend(
        # Input variables:
        lst4dts:list[str],                   # Names of datasets
        data_list:list[xr.DataArray],        # Research datasets at the same order as **lst4dts**
        var:str,                             # Research parameter.
        fire_xarray: Optional[bool] = True,  # Are you working with fire_xarray.py script?
        fire_ratio: Optional[bool] = False,  # Are you working with fire_ratio.py script?
        # OUTPUT variables:
    ) -> list[xr.Dataset]:
    # Start computations:
    # -- Get actual data for TIME TRENDS calculations
    lst4data  = []  # list for data
    lst4years = []  # list for years

    for i in range(len(lst4dts)):
        if fire_xarray == True:
            lst4data.append(data_list[i][var].values)
        elif fire_ratio == True:
            lst4data.append(data_list[i].values)
        lst4years.append(data_list[i].time.dt.year.values )
       # lst4years.append(data_list[i].year.values )

    # -- Get actual time trends
    lst4trends = []
    for i in range(len(lst4dts)):

        # Datasets have NaN values for water objects. Such points shoud be 
        # changed to zero        
        lst4data[i][np.isnan(lst4data[i])] = 0

        # Reshape to an array with as many rows as years and as
        # many columns as there are pixels
        val = lst4data[i].reshape(len(lst4years[i]), -1)
        # Do a first-degree polyfit
        regressions = np.polyfit(lst4years[i], val, 1)
        # Get the coefficients back
        trends = regressions[0,:].reshape(lst4data[i].shape[1],
                                          lst4data[i].shape[2])

        lon = data_list[i].lon.values
        lat = data_list[i].lat.values
        
        trends = xr.DataArray(trends,
                              coords = dict(lat =  lat, lon =  lon),
                              name = 'trends')
        lst4trends.append(trends)
    return lst4trends

# get_difference --> Get values for comparsion differences between different
#                    datasets. (for example: diff = ESA MODIS - OCN)
def get_difference(
        # Input variables:
        dtset_list:list[str],          # List of datasets
        refer_ds:str,                  # Reference dataset (for example: MODIS)
        comp_ds:str,                   # Research dataset (for example: OCN)
        dt_list:list[xr.DataArray],    # Data list for comparison (for example: mean, std, trend lists)
        # OUTPUT variables:
    ) -> list[xr.DataArray]:           # List of parameters in comp_ds grid (reference_ds, comparison_ds, diff).
    # Start computations:
    lst4param  = []
    # Define reference and research datasets (simulations)
    for i in range(len(dtset_list)):
        if dtset_list[i] == refer_ds:
            ref_data = dt_list[i]
        elif dtset_list[i] == comp_ds:
            comp_var = dt_list[i]
    # Get difference
    diff = ref_data - comp_var
    # Create lists
    lst4param.extend([ref_data, comp_var, diff])          
    return lst4param
