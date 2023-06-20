# -*- coding: utf-8 -*-
"""
Task : Comparison fFire results with different grid resolutions

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-10-13 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.3    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================     Import modules     ==================
# --  Standard:
import os
import sys
import xarray as xr
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.path_settings import get_path_in, output_path
from libraries.lib4xarray import comp_area_lat_lon
from libraries.lib4sys_support import makefolder
from libraries.lib4upscaling_support import get_upscaling_ba
from libraries.lib4visualization import create_fast_xarray_plot as xrplot
from libraries.lib4visualization import netcdf_line_plots as nlplot
from libraries.lib4visualization import simple_line_plot_settings
# ========================   Personal functions   =======================

# =============================   User settings   ======================

# -- Define and create output folder :
pout = makefolder(output_path().get('ffire_test'))
print(f'Your data will be saved at {pout}')
# -- Plot settings for linear plot:
user_line_settings = {
    'labels' : ['GFED4.1s_720-1440', 'GFED4.1s_360-720'],
    'colors' : ['b', 'r'],
    'styles' : ['-', '-.'],
    'title'  : 'test_fFire',
    'xlabel' : 'years',
    'ylabel' : 'fFire',
    'xlims'  : [ 2000, 2017, 2  ],
    'ylims'  : [  0.0, 8.01, 2.0],
    'output' : pout + 'annual_fFire.png',
}

# -- Plot settings for 2D maps:
user_map_settings = {
    'fFire_orig' : {
        'robust'   : True,
        'colormap' : 'hot_r',
        'vmin'     :  0.0,
        'vmax'     : 80.0,
        'col'      : None,
        'col_wrap' : None,
        'title'    : 'fFire before upscalling',
        'output'   : pout + 'fFire_720_1440.png',
    },
    'fFire_new' :{
        'robust'   : True,
        'colormap' : 'hot_r',
        'vmin'     :  0.0,
        'vmax'     : 80.0,
        'col'      : None,
        'col_wrap' : None,
        'title'    : 'fFire after upscalling',
        'output'   : pout + 'fFire_360_720.png',
    },
}
# Recalculation coefficients:
g2pg = 1e-15
# =============================    Main program   ======================
if __name__ == '__main__':
    # -- Define input and output paths a
    pin, res_param  = get_path_in(['GFED4.1s'], 'fFire')
    # -- Reading data:
    ncfile = xr.open_dataset(pin[0])
    # -- Rename attribute:
    ncfile['fFire'] = ncfile['C']
    # -- Add field area variable:
    ncfile = ncfile.assign(xr.Dataset({'area': (('lat', 'lon'),
                              comp_area_lat_lon(ncfile.lat.values,
                                                ncfile.lon.values))},
                              coords = {'lat' : ncfile.lat.values,
                                        'lon' : ncfile.lon.values}))
    # -- Convert units:
    param = ncfile['fFire'] * ncfile['area'] * g2pg

    test_fFire = param.to_dataset(name = 'fFire')
    res360_720 = get_upscaling_ba(test_fFire, 'fFire', lreport = True)
    # Values before upscalling:
    x = param.sum(dim = {'lat', 'lon'}).groupby('time.year').sum()
    # Values after  upscalling:
    y = res360_720.sum(dim = {'lat', 'lon'}).groupby('time.year').sum()
    # Add data to a visualization list:
    lst4data = [x, y]

    # -- Plot 1: linear plot with fFire data:
    pic_lplot = nlplot(
        len(lst4data),
        lst4data,
        user_line_settings.get('labels'),
        user_line_settings.get('colors'),
        user_line_settings.get('styles'),
        False,
    )
    # Apply user settings for linear plot:
    simple_line_plot_settings(pic_lplot, user_line_settings)
    # -- Plot 2: Global map with fFire before upscalling:
    xrplot(ncfile['fFire'].mean(dim = {'time'}), 'fFire_orig', user_map_settings)
    # -- Plot 3: fFire after upscalling (should decrease in 4 time as our pixel is bigger in 4 times)
    res360_720 = get_upscaling_ba(ncfile, 'fFire', lreport = True)
    res360_720 = res360_720.to_dataset(name = 'fFire')
    xrplot((res360_720['fFire']/4).mean(dim = {'time'}), 'fFire_new', user_map_settings)
#=============================    End of program   ============================
