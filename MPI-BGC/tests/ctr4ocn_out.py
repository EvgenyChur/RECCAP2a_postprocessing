# -*- coding: utf-8 -*-
"""
Script for controlling output parameter of OCN model at different steps of 
postprocessing. 
    a. Direct output from OCN model - data for one CLUMP;
    b. Data after aggregation of data for global map (all CLUMPs together)
    c. Data after TRENDY output postprocessing

Autors of project: Evgenii Churiulin, Ana Bastos
                                                   
Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de


History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    2022-09-15 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project 
    1.3    2023-02-13 Evgenii Churiulin, MPI-BGC
           Updated output variables
    1.4    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
# -- Standard:
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings import logical_settings
# =============================   Personal functions   ==================

# get_ocn -->
def get_ocn(
        # Input variables:
        data:str,             # Input path to initial data
        var:str,              # Research parameter
        tstep:int,            # Number of the research moment of time (36 = 2003-01-01)
        fyr:str,              # First year (data available from ... to ...)
        lyr:str,              # Last year  (data available from ... to ...)
        mode:str,             # Which type of data you want to use (original or experimental)
        # Output variables:
    ) -> xr.DataArray:        # Data for the research parameter at tstep moment of time.
    # -- Start function:
    ncfile = (xr.open_dataset(data, decode_times = False)
                 .assign_coords({'time': pd.date_range(fyr, lyr, freq = '1M')}))  
    if mode == 'orig':
        return ncfile[var][tstep,:,:,:]
    else:
        return ncfile[var][tstep,:,:]
        


# =============================    Main program   ======================
if __name__ == '__main__':

    # =============================   User settings   =======================
    # Do you want to calculate on cluster?
    lcluster = logical_settings(lcluster = True).get('lcluster')
    # Current user:
    user = 'evchur'
    # Time step (36 is equal to 2003-01-01):
    tstep = 36
    # Data type -> 'orig' or 'exp':
    dtype = 'exp'

    # Define output paths:
    if lcluster:
        main = '..'
        scratch      = main + f'/scratch/{user}/OCN/RUNDIR/RECCAP2A_v4_rev294'
        people_step2 = main + f'/people/{user}/Models/OCN/results/RECCAP2A_v4_rev294/MAPS'
        people_step3 = main + f'/work_1/RECCAP2/RECCAP2A/v202309/OCN/S2Diag'

        # -- Original OCN values:
        if dtype == 'orig':
            paths = [
                scratch      + '/S2Diag_orig/Out/553/mFIREFRAC_2000-2010.nc',       # direct OCN output
                people_step2 + '/S2Diag_orig/mFIREFRAC_2000-2010_S2Diag.nc',        # OCN output postprocessing (f90)
                people_step3 + '/OCN_S2Diag_orig_firepft.nc',                       # OCN trendy output (data after trendy output)
            ]
            fst_yr = '2000-01-01'
            lst_yr = '2011-01-01'
        # -- Experiment OCN values (OCN_v202302):
        else:
            paths = [
                scratch      + '/S2Diag/Out/553/mFIREFRAC_2003-2020.nc',
                people_step2 + '/S2Diag/mFIREFRAC_2003-2020_S2Diag.nc',
                people_step3 + '/OCN_S2Diag_firepft.nc',
            ]
            fst_yr = '2000-01-01'
            lst_yr = '2021-01-01'
    # Working with local computer copy of data:
    else:
        main = f'C:/Users/{user}/Desktop/DATA'
        # -- Original OCN values:
        if dtype == 'orig':
            paths  = [
                main + '/OCN_ORIG/mFIREFRAC_2000-2010.nc',                          # Direct OCN output
                main + '/OCN_ORIG/mFIREFRAC_2000-2010_S2Diag.nc',                   # OCN output postprocessing (f90)
                main + '/OCN_ORIG/OCN_S2Diag_firepft.nc',                           # OCN trendy output (data after trendy output)
            ]
            fst_yr = '2000-01-01'
            lst_yr = '2011-01-01'
        else:
            # -- Experiment OCN values:
            paths  = [main + '/OCN_TEST/mFIREFRAC_2000-2020.nc',
                      main + '/OCN_TEST/mFIREFRAC_2000-2020_S2Diag.nc',
                      main + '/OCN_TEST/OCN_S2Diag_firepft.nc'        ]
            fst_yr = '2000-01-01'
            lst_yr = '2021-01-01'


    # -- Get data (Step 1, step 2, step 3):
    tbaf        = get_ocn(paths[0], 'FIREFRAC', tstep, fst_yr, lst_yr, dtype).sum(dim = {'PFT'}).data
    tbaf_s2Diag = get_ocn(paths[1], 'FIREFRAC', tstep, fst_yr, lst_yr, dtype)
    btaf_trendy = get_ocn(paths[2], 'firepft' , tstep, fst_yr, lst_yr, dtype).sum(dim = {'vegtype'}).data
    # -- Select tbaf CLUMP from global map:
    tbaf_s2Diag14 = tbaf_s2Diag[  13, 182:196, 576:594].data                        # problem with this values. TRENDY uses it
    tbaf_s2Diag   = tbaf_s2Diag[0:13, 182:196, 576:594].sum(dim = {'pft'}).data
    btaf_trendy   = btaf_trendy[182:196, 576:594]
    # -- Check values:
    for i in np.arange(0,14,1):      # Latitudes
        for j in np.arange(0,18,1):  # longitudes
            # -- Control values between tbaf and tbaf_s2Diag:
            if tbaf[i,j] != tbaf_s2Diag[i,j]:
                print('There is a problem at pixel:', i, j, 'STEP 1')
                sys.exit()
            # -- Control values between tbaf and btaf_trendy:
            if tbaf[i,j] != tbaf_s2Diag[i,j]:
                print('There is a problem at pixel:', i, j, 'STEP 2')
                sys.exit()
            # -- Control values between tbaf_s2Diag and btaf_trendy:
            if tbaf_s2Diag[i,j] != btaf_trendy[i,j]:
                print('There is a problem at pixel:', i, j, 'STEP 3')
                sys.exit()
# =============================    End of program   =====================
