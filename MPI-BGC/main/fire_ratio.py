# -*- coding: utf-8 -*-
"""
Creating a collage with the carbon ration (fFire / burned Area) plots:

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-08-02 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-12 Evgenii Churiulin, MPI-BGC.
           Updated functions according with the new updates into xrlib
    1.3    2022-10-28 Evgenii Churiulin, MPI-BGC.
           Updated functions according with the new updates into xrlib
    1.4    2022-11-15 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.5    2023-02-13 Evgenii Churiulin, MPI-BGC
           Updated output and input functions
    1.6    2023-05-24 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     =================
# 1.1: Standard modules
import os
import sys
# -- Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.user_settings import time_limits
from settings.path_settings import get_path_in, output_path
from calc.stat_controls import timmean, timstd, timtrend
from calc.vis_controls import collage_plot
from libraries.lib4xarray import get_data, get_interpol
from libraries.lib4sys_support import makefolder
from libraries.lib4visualization import create_fast_xarray_plot as xrplot
# =============================   Personal functions   =================
# -- read_data --> Get data presented on OCN grid for your research parameter:
def read_data(
        # Input variables:
        region:str,               # Research domain (Global, Europe, Other..);
        lst4datasets:list[str],   # Research dataset names;
        var :str,                 # Research parameter (common for all -> nc attribute);
        linfo:bool,               # Do you want to get more information about data?
        # Output variables:
    ) -> tuple[list]:             # Research data presented on OCN grid
    # -- Start computations:
    # -- Get data paths and NetCDF attributes:
    ipaths, res_param = get_path_in(lst4datasets, var)
    # -- Read data:
    lst4data = get_data(
        ipaths, lst4datasets, var, res_param, linfo = linfo, lresmp = True)
    # -- Upscalling data:
    lst4data = get_interpol(lst4data, lst4datasets, region, var)
    return lst4data

# ================   User settings (have to be adapted)  ===============
# -- Logical parameteres:
# Do you want to get more information about data?
linfo = False
# -- Define output paths and create folder for results:
data_OUT = makefolder(output_path().get('fire_ratio'))
print(f'Your data will be saved at {data_OUT}')
# -- Settings for work:
# Research region ('Global', 'Europe', 'Tropics', 'NH', 'Other')
region = 'Europe'
# Parameter for burned area:
param_ba = 'burned_area'
# Parameter for fFire:
param_fFire = 'fFire'
# OCN data + Research datasets:
dtset_list  = ['OCN_S2Prog', 'OCN_S2Diag', 'GFED4.1s']
# -- Settings for simple plot with differences:
plt_settings = {
    'plot_BA_diff' : {
        'robust'   : True,
        'colormap' : 'hot_r',
        'vmin'     : 0.0,
        'vmax'     : 30.0,
        'col'      : None,
        'col_wrap' : None,
        'title'    : 'Burned area coefficients',
        'output'   : data_OUT + f'ba_coef_{region}.png',
    },
    'plot_fFire_diff' : {
        'robust'   : True,
        'colormap' : 'hot_r',
        'vmin'     : 0.0,
        'vmax'     : 30.0,
        'col'      : None,
        'col_wrap' : None,
        'title'    : 'Fire emission coefficients',
        'output'   : data_OUT + f'ffire_coef_{region}.png',
    },
}
# -- Settings for collage plot:
# Y axis laber
bm_ylabel   = 'fFire/BA, kgC m\u207b\u00B2 yr\u207b\u00B9'
# plot title
c_title     = f'Ratio of CO2 fire emission to burned area over {region} region'
# Output path for collage plot
c_path_OUT  = data_OUT + f'carbon_ration_{region}.png'

# Colormaps range and color
colorbar_limits = [
    {'mode' :'ratio',
     'param':'mean',
     'ymin' :  0.0,
     'ymax' : 10.0,
     'cbar' : 'hot_r',
    },
    {'mode' :'ratio',
     'param':'std',
     'ymin' :  0.0,
     'ymax' :  1.0,
     'cbar' : 'hot_r',
    },
    {'mode' :'ratio',
     'param':'trend',
     'ymin' : -1e-1,
     'ymax' :  1e-1,
     'cbar' : 'bwr',
    }
]

# -- Recalculation coefficients:
g2kg = 1e-3
km2m = 1e9
# =============================    Main program   ======================
if __name__ == '__main__':
    print('START program')
    # -- Get burned area and fFire data:
    lst4ba = read_data(region, dtset_list, param_ba, linfo)
    lst4fFire = read_data(region, dtset_list, param_fFire, linfo)
    # -- Test for coefficients
    ba_coef = ((lst4ba[1]['burned_area']).mean('time') /
               (lst4ba[0]['burned_area']).mean('time') )

    ffire_coef = ((lst4fFire[1]['fFire']).mean('time') /
                  (lst4fFire[0]['fFire']).mean('time') )
    # -- Create simple plots for understanding:
    xrplot(ba_coef, 'plot_BA_diff', plt_settings)
    xrplot(ffire_coef, 'plot_fFire_diff', plt_settings)
    # -- Convert data and get metric for analysis:
    data_final = []
    for i in range(len(dtset_list)):
        # gC m-2 yr-1 --> gC yr-1:
        temp_res = (
            (lst4fFire[i]['fFire'] * lst4fFire[i]['area'] * g2kg) /
            (lst4ba[i]['burned_area'] * km2m))
        data_final.append(temp_res)
    # -- Get statistical values (MEAN, STR, TRENDs):
    lst4mean = timmean(
        dtset_list,
        data_final,
        var = None,
        fire_xarray = False,
        fire_ratio = True,
    )
    lst4std  = timstd(
        dtset_list,
        data_final,
        var = None,
        fire_xarray = False,
        fire_ratio = True,
    )
    lst4trends = timtrend(
        dtset_list,
        data_final,
        param_ba,
        fire_xarray = False,
        fire_ratio = True,
    )
    # -- Get actual latitudes and longitudes for each dataset:
    lst4lat  = []
    lst4lon  = []
    for i in range(len(data_final)):
        lst4lat.append(data_final[i].lat.values)
        lst4lon.append(data_final[i].lon.values)
    # -- Create collage plot (mean, std, trend):
    print(f'Collage mode - Plot data for {region} region')
    collage_plot(
        dtset_list,
        region,
        lst4lon,
        lst4lat,
        lst4mean,
        lst4std,
        lst4trends,
        'ratio',
        bm_ylabel,
        c_title,
        c_path_OUT,
        ldiff = False,
        clb_uniq = colorbar_limits,
    )
    print('END program')
# =============================    End of program   ====================
