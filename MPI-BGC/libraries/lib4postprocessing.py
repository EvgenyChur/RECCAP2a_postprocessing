# -*- coding: utf-8 -*-

"""
Module with postprocessing functions for work with burned area data.

P.S.: You have to use this script before `fire_xarray.py`!!!

Idea: 
    Case 1. ESA-CCI MODIS data:
        We have 18 different PFT into the original ESA-CCI data, however the OCN
        model does not work with crops. Because of that we have prepared the
        special data for OCN model with total values of burned area which was
        calculated based on 15 ESA-CCI PFT (first 3 PFTs were excluded from
                                            calculations).
        The main task of this script is changing the original values of burned 
        area in burned_area to total burned area based on 15 pft. The output
        parameters should be the same as in fire_xarray and user_settings modules.

    Case 2. OCN data:
        We have data for 13 PFT. Task: get total values and write them to the
        field burnedArea. As it was before. The output parameters should
        be the same as in fire_xarray and user_settings modules.

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-10-21 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-11 Evgenii Churiulin, MPI-BGC
           Add call function from different place
    1.3    2023-05-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================     Import modules     ====================
import pandas as pd
import xarray as xr
from typing import Optional
# =============================   Personal functions   ====================

# ba_postprocessing --> Reading NetCDF data using one of 2 available algorithms and
#                       changing burned area data:
#                       a) OCN - get total burned area;
#                       b) ESA-CCI MODIS -> get total burned area over natural PFT.
#                       Save new dataset in new NetCDF file:
def ba_postprocessing(
    # Input variables:
    pin:str,                           # Input path
    pout:str,                          # Output path
    nvar:str,                          # Name of the research attribute in NetCDF
    npft:str,                          # Name of the PFT attribute in NetCDF
    mode:str,                          # Type of data for analysis (OCN or ESA-CCI MODIS)
    frs_yr: Optional[str] = None,      # First year of the research period. Default is None
    lst_yr: Optional[str] = None,      # Last year of the research period. Default is None
    steps: Optional[str] = None        # Time step. The default is None
    # OUTPUT variables:
    ) -> xr.Dataset:                   # Dataset with corrected data. Also, the same
                                       # file was saved in NetCDF format for further manipulations.

    # -- Open dataset and change original values to the new one
    if mode == 'OCN':
        ds = (xr.open_dataset(pin, decode_times = False)
                .assign_coords({'time': pd.date_range(frs_yr, lst_yr, freq = steps)})
        )
        # Change data in file:
        ds[nvar] = ds[nvar].sum(dim = {npft})
        ntba_pft = ds[nvar].to_dataset(name = nvar)
        # # Save file:
        ntba_pft.to_netcdf(pout)
        return ntba_pft
    # MODIS dataset
    else:
        natural_pft = 3 # Natural PFTs are from index 3:
        ds = xr.open_dataset(pin)
        # Change data in file:
        ds['burned_area'] = ds[nvar][:, natural_pft:, :, :].sum(dim = {npft})
        # Save file:
        ds.to_netcdf(pout)
        return ds
