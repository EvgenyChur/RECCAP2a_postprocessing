# -*- coding: utf-8 -*-
__all__ = [
    'get_path_in',
    'get_parameters',
    'get_output_path',
]
"""
Get actual paths and parameters for the research datasets and OCN simulations.

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-06-22 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
    1.2    2022-09-22 Evgenii Churiulin, MPI-BGC
           Updated get_path_in and get_parameters subroutines
    1.3    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
           changed - machine to lcluster, changed functions input parameteres
    1.4    2023-05-08 Evgenii Churiulin, MPI-BGC
           Code refactoring
    1.5    2023-09-11 Evgenii Churiulin, MPI-BGC
           Updated functions according to the changes in user settings. Function
           output_path was renamed to get_output_path. Added parameters for packedge
           import
"""
# =============================     Import modules     ===================
import os
import sys
import xarray as xr
import pprint

import mlocal_set
import mcluster_set
from user_settings import logical_settings

# ========================   Personal functions   ========================

# 1. get_path_in -> Get actual input path for input models (OCN, JULES, ORCHIDEE)
#                   or satellite datasets
def get_path_in(
        # Input variables:
        lst4dts:list[str],             # Research datasets (just names)
        var:str,                       # Research parameter (burned_area, gpp, npp ant ets.)
        lsettings:dict,                # User logical settings
        # OUTPUT variables:
    ) -> tuple[list[str],              # Input data paths (absolute path)
               list[str]]:             # NetCDF attribute names of the research datasets
    #print(lst4dts)
    # -- Local parameters:
    ocn_id, jules_id, orchidee_id = 'OCN', 'JUL', 'ORC'

    # -- Define settings for local or cluster computer
    if lsettings.get('lcluster'):
        # -- Satellite and model datasets different from OCN, JULES, ORCHIDEE
        dts_cat          = mcluster_set.datasets_catalog()
        # OCN data
        ocn_cat, ocn_atb = mcluster_set.ocn_catalog(var)
        # -- JULES data
        jul_cat, jul_atb = mcluster_set.jules_catalog(var)
        # -- ORCHIDEE data
        orc_cat, orc_atb = mcluster_set.orchidee_catalog(var)
    else:
        dts_cat          = mlocal_set.loc_datasets_catalog()
        ocn_cat, ocn_atb = mlocal_set.loc_ocn_catalog(var)
        jul_cat, jul_atb = mlocal_set.loc_jules_catalog(var)
        orc_cat, orc_atb = mlocal_set.loc_orchidee_catalog(var)

    # 2. Get actual data paths
    catalog   = []
    res_param = []
    for dt_set in lst4dts:
        # -- Use settings for OCN data:
        if dt_set[0:3] == ocn_id:
            fpath  = ocn_cat.get(dt_set)
            nc_atb = ocn_atb.get(var)
        # -- Use settings for JULES data
        elif dt_set[0:3] == jules_id:
            fpath  = jul_cat.get(dt_set)
            nc_atb = jul_atb.get(var)
        # -- Use settings for ORCHIDEE data
        elif dt_set[0:3] == orchidee_id:
            fpath  = orc_cat.get(dt_set)
            nc_atb = orc_atb.get(var)
        # -- Use settings for datasets
        else:
            for item in dts_cat:
                if (item['mode'] == var and item['dataset'] == dt_set):
                    fpath  = item['path']
                    nc_atb = item['attribute']

        # -- Create paths and attributes lists 
        catalog.append(fpath)
        res_param.append(nc_atb)
    return catalog, res_param


def get_parameters(
        # Input variables:
        lst4dts:list[str],                  # Research datasets (just names)
        var:str,                            # Research parameter (burned_area, gpp, npp ant ets.)
        lsettings:dict,                     # User logical settings
        # OUTPUT variables:
    ) -> tuple[str,                         # Short name of the research parameter (s_name)
               str,                         # Full name of the research parameter (l_name)
               str,                         # Units for 2D plot
               str]:                        # Units for 3D plot (units can be different)
    """Get correct data names (short and full) and units for using this
    information as a source of data for linear, 2D, 3D and collage plots. """
    # -- Define actual parameters for simulations and datasets:
    var_units = mcluster_set.dataset_units() if lsettings.get('lcluster') else mlocal_set.loc_dataset_units()

    # -- Get actual parameters for datasets:
    for item in var_units:                                   # cycle by dictionary elements
        if (item['mode'] == var):                            # select parameter
            # 3.2. Get other parameters:
            s_name  = item['short_name']
            l_name  = item['axis_name']
            unit_2d = item['units4line']
            unit_3d = item['units4collage'] 
    
    return s_name, l_name, unit_2d, unit_3d


# 3. Get output path for calculation results:
def get_output_path(lsettings:dict) -> dict:
    """Define actual parameters for simulations and datasets:"""
    return (
        mcluster_set.output_folders() if lsettings.get('lcluster') else mlocal_set.loc_output_folders()
    )

if __name__ == '__main__':
    # =============================   User settings   ==================

    # -- Define actual datasets (Potential options):
    lst4dts = ['OCN_Spost_v4', 'OCN_S0_v4', 'OCN_S2Prog_v4', 'OCN_S2Diag_v4']
    # -- Define the main focus of data for analysis:
    var = 'burned_area' # 'lai', 'fFire', 'gpp'
    # -- Define logical settings:
    lsets = logical_settings(lcluster = True)

    # =============================    Main program   ==================
    # -- Get INPUT paths:
    pin, res_param = get_path_in(lst4dts, var, lsets)
    # -- Get list of actual parameters:
    s_var_name, var_name, lplot_units, cplot_units = get_parameters(lst4dts, var, lsets)
    # -- Get list of output paths:
    pout = get_output_path(lsets)

    print('Actual input paths:', pin, '\n')
    print('Actual parameters:' , res_param, '\n')
    print('Actual output path:', pout, '\n')
    # -- Open file (test mode):
    for path in pin:
        print(f'Data reading test. Actual dataset is {path}')
        nc = xr.open_dataset(path, decode_times = False)
    # =============================    END program   ===================
