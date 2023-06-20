# -*- coding: utf-8 -*-

"""
Task: Comparison of burned area values from OCN model and ESA-CCI MODIS for 4
      different vegetation groups and several subgroups:

Next PFT from OCN model were included in:
    1. CROPS + BS and Flooded Trees  --> Bare soil + C3/C4 agriculture
    2. Evergreen trees (EBF and ENF) --> Broadleaved  evergreen (Tropical , Temperate)
                                         Needleleaved evergreen (Temperate, Boreal   )
    3. Deciduous trees (DNF and DBF) --> Broadleaved  deciduous (Tropical, Temperate, Boreal)
                                         Needleleaved deciduous (Boreal) 
    4. Grass and shrubs              --> C3 / C4 grass    

Next PFT from ESA were included in:
    1. CROPS + BS and Flooded Trees  --> Cropland, rainfed
                                         Cropland, irrigated or post-flooding
                                         Mosaic cropland (>50%) / natural vegetation (<50%)
                                         Mosaic natural vegetation (>50%) / cropland (<50%)
                                         Lichens and mosses
                                         Sparse vegetation (tree, shrub, herbaceous cover) (<15%)
                                         Tree cover, flooded, fresh or brackish water
                                         Tree cover, flooded, saline water
                                         Shrub or herbaceous cover, flooded, fresh/saline/brakish water

    2. Evergreen trees (EBF and ENF) --> Evergreen trees: broadleaved and
                                         needleleaved (closed to open (>15%)) +
                                         mixed leaf type

    3. Deciduous trees (DNF and DBF) --> Deciduous trees: broadleaved and
                                         needleleaved (closed to open (>15%))

    4. Grass and shrubs              --> Grassland

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    11.10.2022 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-15 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.3    2023-05-15 Evgenii Churiulin, MPI-BGC
           Code refactoring + transfered pft_plot function to calc/vis_control.py
"""
# =============================     Import modules     ==================
# -- Standard modules:
import os
import sys
import xarray as xr

# -- Personal module:
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4xarray import get_data, get_interpol
from libraries.lib4upscaling_support import get_upscaling_ba_veg_class
from libraries.lib4sys_support import makefolder
from libraries.lib4colors import check_colors
from settings.path_settings import get_path_in, output_path
from calc.vis_controls import pft_plot
# =============================   Personal functions   ==================
# 1. read_data --> Reading burned area actual datasets (model simulations) and
#                  converting them into OCN grid (720*300):
def read_data(
                # Input variables:
                region:str,                       # Research domain (Global, Europe, Other..)
                lst4datasets:list[str],           # Research datasets
                ipaths:list[str],                 # Input dataset paths
                var:str,                          # Research parameter
                param_var:str,                    # NetCDF attributes for research datasets
                linfo:bool,                       # Do you want to get more information about your NetCDF?
                dtype:str,                        # Main source of incoming data (OCN, ESA)
                # Output variables:
            ) -> xr.DataArray:                    # Research dataset presented on OCN grid
    # -- Read in data:
    lst4data = get_data(
        ipaths, lst4datasets, var, param_var, linfo = linfo, lresmp = True)
    # Upscalling data 
    if dtype == 'OCN':
        lst4data = get_interpol(lst4data, lst4datasets, region, var)  
        ds_final = lst4data[0][var]
    else:
        ds_final = get_upscaling_ba_veg_class(
            lst4data[0], param_var[0], lreport = True , lplot = False,
        )
    return ds_final

# =============================   User settings   ==========================
# -- Logical parameteres:
# Do you want to get more information about data?
linfo    = False

# -- Main settings:
# Research region ('Global', 'Europe', 'Tropics', 'NH')
region   = 'Global'
# OCN simulations: OCN_S2.1, _S2.2, _S3.1, _S3.2, _S2Prog, _S2Diag
ocn_sims = ['OCN_S2Diag']
# ESA-CCI data
lst4esa  = ['BA_MODIS']
# Research parameter
var      = 'burned_area'
# OCN NetCDF attribute name (burned area):
ocn_var  = 'burnedArea'
# OCN NetCDF attribute name (vegetation):
ocn_pft  = 'vegtype'
# ESA NetCDF attribute name (burned area):
esa_var  = 'burned_area_in_vegetation_class'
# ESA NetCDF attribute name (vegetation):
esa_pft  = 'vegetation_class'

# -- Settings for linear plot:
plt_settings = {
    # Settings for CROPS + BS and Flooded Trees:
    'crops'   : {
        # ptype    parameter    Relevant values
        'legend' : ['OCN - CROPS + BS', 'ESA - CROPS + BS', 'ESA - Flooded Trees'],
        'color'  : check_colors.get(3).get('color'),
        'style'  : check_colors.get(3).get('style'),
        'ylim'   : [  0.0, 1000.1, 250.0],
    },
    # Settings for evergreen trees (EBF and ENF):
    'evgreen' : {
        'legend' : ['OCN - ENF', 'OCN - EBF', 'ESA - ENF', 'ESA - EBF'],
        'color'  : check_colors.get(4).get('color'),
        'style'  : check_colors.get(4).get('style'),
        'ylim'   : [  0.0, 500.1, 50.0],
    },
    # Settings for deciduous trees (DNF and DBF):
    'decid'   : {
        'legend' : ['OCN - DNF', 'OCN - DBF', 'ESA - DNF', 'ESA - DBF'],
        'color'  : check_colors.get(4).get('color'),
        'style'  : check_colors.get(4).get('style'),
        'ylim'   : [  0.0, 2500.1, 500.0],
    },
    # Settings for grass and shrubs:
    'grass'   : {
        'legend' : ['OCN - Grass', 'ESA - Grass', 'ESA - Shrubs'],
        'color'  : check_colors.get(3).get('color'),
        'style'  : check_colors.get(3).get('style'),
        'ylim'   : [  0.0, 3000.1, 500.0],
    },
}

# 3.5 PFT groups for OCN and ESA-CCI MODIS data
#             CROPS + BS   ENF  EBF  DNF  DBF  Grass  Shrub   Flooded
ocn_groups = [    0.0   ,  0.0, 0.0, 0.0, 0.0, 0.0                   ]
esa_groups = [    0.0   ,  0.0, 0.0, 0.0, 0.0, 0.0  ,  0.0  ,   0.0  ]
#=============================    Main program   ==============================
if __name__ == '__main__':
    print('Program START')
    # -- Define input and output paths and create folder for results:
    # Important information:  pin_param - has None values in this script. Due to there
    #                         is no key attribute from attribute_catalog  of mclister.py
    #                         or mlocal.py modules. Nevertheless, you use this function
    #                         because of input path has correct name and pin_param is
    #                         unused in this script!
    # Input  ESA_CCI MODIS original data
    pin_esa, esa_param  = get_path_in(lst4esa , 'burned_area')
    # Input OCN data
    pin_ocn, ocn_param  = get_path_in(ocn_sims, 'firepft')

    data_OUT = makefolder(output_path().get('check_ocn_pft'))
    print(f'Your data will be saved at {data_OUT}')

    # -- Get data for OCN and ESA-CCI MODIS:
    ba4pft_ocn = read_data(region, ocn_sims, pin_ocn, var, [ocn_var], linfo,
                           'OCN').sel(time = slice('2001', '2018'))

    ba4pft_esa = read_data(region, lst4esa , pin_esa, var, [esa_var], linfo,
                           'ESA').sel(time = slice('2001', '2018'))

    # -- calc_group --> Get relevant data for corresponding plant types
    def calc_group(
                        # Input variables:
                        act_data:xr.DataArray,   # Research dataset
                        pft_groups:list[int],    # PFT groups
                        pft_name:str,            # PFT parameter
                        # Output variables
                   ) -> xr.DataArray:            # Processed data
        return act_data[:, pft_groups, :, :].sum(dim = {pft_name,'lat', 'lon'})

    # -- Create OCN groups:
    ocn_groups[0] = calc_group(ba4pft_ocn, [ 0, 11, 12        ], ocn_pft)       # CROPS + BS
    ocn_groups[1] = calc_group(ba4pft_ocn, [ 3,  6            ], ocn_pft)       # ENF - evergreen needleleaved forest
    ocn_groups[2] = calc_group(ba4pft_ocn, [ 1,  4            ], ocn_pft)       # EBF - evergreen broadleaved forest
    ocn_groups[3] = calc_group(ba4pft_ocn, [ 8                ], ocn_pft)       # DNF - deciduous needleleaved forest
    ocn_groups[4] = calc_group(ba4pft_ocn, [ 2,  5,  7        ], ocn_pft)       # DBF - deciduous broadleaved forest
    ocn_groups[5] = calc_group(ba4pft_ocn, [ 9, 10            ], ocn_pft)       # Grass

    # -- ESA groups:
    esa_groups[0] = calc_group(ba4pft_esa, [ 0,  1, 2, 3      ], esa_pft)       # CROPS + BS
    esa_groups[1] = calc_group(ba4pft_esa, [ 6                ], esa_pft)       # ENF - evergreen needleleaved forest
    esa_groups[2] = calc_group(ba4pft_esa, [ 4,  8            ], esa_pft)       # EBF - evergreen  broadleaved forest
    esa_groups[3] = calc_group(ba4pft_esa, [ 7                ], esa_pft)       # DNF - deciduous needleleaved forest
    esa_groups[4] = calc_group(ba4pft_esa, [ 5                ], esa_pft)       # DBF - deciduous  broadleaved forest
    esa_groups[5] = calc_group(ba4pft_esa, [12                ], esa_pft)       # Grass
    esa_groups[6] = calc_group(ba4pft_esa, [ 9, 10, 11        ], esa_pft)       # Shrubs
    esa_groups[7] = calc_group(ba4pft_esa, [13, 14, 15, 16, 17], esa_pft)       # Flooded wood

    # -- Visualization of model results:
    # 4.3.1 Plot for CROPS + BS and Flooded Trees:
    group = [ocn_groups[0], esa_groups[0], esa_groups[7]]
    pft_plot(group, plt_settings, 'crops', data_OUT)

    # 4.3.2 Plot for evergreen trees (EBF and ENF):
    group = [ocn_groups[1], ocn_groups[2], esa_groups[1], esa_groups[2]]
    pft_plot(group, plt_settings, 'evgreen', data_OUT)

    # 4.3.3 Plot for deciduous trees (DNF and DBF):
    group = [ocn_groups[3], ocn_groups[4], esa_groups[3], esa_groups[4]]
    pft_plot(group, plt_settings, 'decid', data_OUT)

    # 4.3.4 Plot for grass and shrubs:
    group = [ocn_groups[5], esa_groups[5], esa_groups[6] ]
    pft_plot(group, plt_settings, 'grass', data_OUT)

    print('Program END')

#=============================    End of program   ============================ 
