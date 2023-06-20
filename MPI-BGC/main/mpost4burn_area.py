# -*- coding: utf-8 -*-
"""
Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-11-09 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2023-05-15 Evgenii Churiulin, MPI-BGC
           Code rafactoring
"""

# =============================     Import modules     ==================
# 1.1: Standard modules
import os
import sys
# 1.2 Personal module
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4sys_support import makefolder
from libraries.lib4postprocessing import ba_postprocessing
from settings.path_settings import get_path_in, output_path
# =============================   Personal functions   ==================

# =============================   User settings   =======================
#mode    = 'OCN'
mode    = 'MODIS'

# -- Main settings:
# Important information:  pin_param - has None values in this script. Due to there
#                         is no key attribute from attribute_catalog  of mclister.py
#                         or mlocal.py modules. Nevertheless, you use this function
#                         because of input path has correct name and pin_param is
#                         unused in this script!
#
#                         Script is required 2 different output paths (for OCN, for ESA-CCI)
if mode == 'OCN':
    # Input OCN data: pin_param is not active
    pin, pin_param = get_path_in(['OCN_S2Diag_v3'], 'firepft')
    # Output OCN data
    pout     = makefolder(output_path().get('mpost4burn_area_OCN'))
    pout     = pout + 'OCN_S2Diag_burnedArea.nc'
    print(f'Your data will be saved as {pout}')
    # First year
    tstart   = '2003-01-01'
    # Last  year
    tstop    = '2021-01-01'
    tstep    = '1M'
    var_name = 'burnedArea'
    pft_name = 'vegtype'
else:
    # MODIS original
    pin, pin_param = get_path_in(['BA_MODIS'], 'burned_area')           
    # Output OCN data
    pout     = makefolder(output_path().get('mpost4burn_area_MODIS'))
    # natural - except cropts (excluded first 3 PFTs)
    pout     = pout + 'ESACCI-L4_FIRE-BA-MODIS-fv5.1_2001-2018_annual_nat.nc'
    print(f'Your data will be saved as {pout}')
    var_name = 'burned_area_in_vegetation_class'
    pft_name = 'vegetation_class'  

# =============================    Main program   ======================
if __name__ == '__main__':
    print('START program')
    print(mode, '\n')

    # a: Get new OCN data:
    if mode == 'OCN':
        ds_corr = ba_postprocessing(
            pin[0], pout, var_name, pft_name, mode, frs_yr = tstart,
            lst_yr = tstop, steps = tstep,
        )
    # b: Get new MODIS data:
    else:
        ds_corr = ba_postprocessing(pin[0], pout, var_name, pft_name, mode)
    print(ds_corr.info)
    print('END program')
# =============================    End of program   ====================
