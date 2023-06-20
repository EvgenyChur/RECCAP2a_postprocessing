# -*- coding: utf-8 -*-
"""
Description: Testing new GFED data source

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    %(date) Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
    1.2    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================     Import modules     ==================
# -- Standard:
import os
import sys
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4xarray import comp_area_lat_lon
import libraries.lib4upscaling_support as lib4ups
# =============================   Personal functions   ==================

# ================   User settings (have to be adapted)  ================
# Input paths:
mpath = 'C:/Users/evchur/Desktop'
gfed_path = mpath + '/GFED_annual_burned_area_2002-2020_025d.nc'
# Research parameter:
lparam = 'burned_area'
# Recalculation coefficient:
rec_coef = 1e-9

# =============================    Main program   =======================
if __name__ == '__main__':
    # -- Open NetCDF:
    ncfile = xr.open_dataset(gfed_path)
    # -- Add area field:
    ncfile = ncfile.assign(xr.Dataset({'area': (('lat', 'lon'),
                                   comp_area_lat_lon(ncfile.lat.values,
                                                     ncfile.lon.values))},
                                   coords = {'lat' : ncfile.lat.values,
                                             'lon' : ncfile.lon.values}))
    # -- Units convertation:
    ncfile[lparam] = (ncfile[lparam] * ncfile['area'] * rec_coef)
    # -- Re-interpolation:
    gfed_ba = lib4ups.get_upscaling_ba(ncfile, lparam, lreport = True)
# =============================    End of program   =====================



