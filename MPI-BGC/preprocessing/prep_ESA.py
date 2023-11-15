# -*- coding: utf-8 -*-
"""
Program for preprocessing ESA-CCI MODIS_f5.1s burned area data for OCN model

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-09-09 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-24 Evgenii Churiulin, MPI-BGC
           Rewritten
    1.3    2022-11-14 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.4    2023-06-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================== Import modules =======================
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
import time
import subprocess
import numpy as np
import pandas as pd

from settings import logical_settings, get_path_in, get_output_path, config
from libraries import makefolder, get_data, comp_area_lat_lon, get_upscaling_ba_veg_class
from libraries import create_fast_xarray_plot as xrplot
from libraries import create_lplot_with_2axis as lplot2axis


# =============================== User functions =======================
def get_data_vis(dataset, col):
    x = pd.concat(dataset, axis = 0)
    df = x.reset_index().set_index(x[0]).drop(['index', 0], axis = 1).astype('float')
    df.columns = [col]
    return df



if __name__ == '__main__':
    # ============================= Users settings =========================
    # -- Load basic logical settings:
    lsets = logical_settings(lcluster = True)
    # -- Load other logical parameters:
    lzero = False  # Do you have unzip raw files?
    nc_prep = False # Do you want to preprare new netcdf for OCN?
    lplot = False   # Do you want to plot data?

    # -- Load basic user settings:
    bcc = config.Bulder_config_class()
    tlm = bcc.user_settings()

    # -- Get output paths and create folders for results:
    # Output path for new NetCDF data:
    data_out = makefolder(get_output_path(lsets).get('prep_ESA_data'))
    print(f'Your data will be saved at {data_out}')
    # Output path for figures:
    fig_out  = makefolder(get_output_path(lsets).get('prep_ESA_fig'))
    print(f'Your figures will be saved at {fig_out}')

    # -- Settings for plots:
    if lplot:
        # -- Plot settings for linear plot:
        user_line_settings = {
            'labels'     : ['Total BA - 0.25 grid', 'Total BA frac - 0.25 grid',
                            'Total BA - 0.5 grid' , 'Total BA frac - 0.5 grid'],
            'colors'     : ['darkblue', 'royalblue', 'brown',  'red'],
            'styles'     : [  '-.'    ,    '-'     ,   '--' ,   '-' ],
            'columns'    : ['ba'      , 'baf'      ,   'ba' ,  'baf'],
            'title'      : 'Comparison of burned area and fraction before interpolation and after',
            'ylabel_ax1' : 'Total burned area, m2',
            'ylabel_ax2' : 'Total burned area fraction',
            'clr'        : 'black',
            'fsize'      : 14.0,
            'pad'        : 20.0,
            'rotation'   :  0.0,
            'loc_ax1'    : 'upper left',
            'loc_ax2'    : 'upper right',
            'leg_frameon': True,
            'output'     : fig_out + '/fire_com.png',
        }
        # -- Settings for 2D maps
        user_map_settings = {
        'fire_025' : {
            'robust'   : True,
            'colormap' : 'hot_r',
            'vmin'     :  0.0,
            'vmax'     :  1.0,
            'col'      : 'time',
            'col_wrap' :  4,
            'title'    : 'Fire fraction at 0.25 degree grid',
            'output'   : '',
            },
        'fire_050' : {
            'robust'   : True,
            'colormap' : 'hot_r',
            'vmin'     :  0.0,
            'vmax'     :  1.0,
            'col'      : 'time',
            'col_wrap' :  4,
            'title'    : 'Fire fraction at 0.5 degree grid',
            'output'   : '',
            },
        }

    # -- Settings for available ESA-CCI data.
    #    NDEP always the same (use only for coordinates and attributes comparison)
    #years = np.arange(2001, 2021, 1)
    years  = np.arange(2001, 2003, 1)
    lparam = 'burned_area'                      # name of parameter which I'm using for reading and initial processing of data
    nvar   = 'burned_area_in_vegetation_class'  # NetCDF attribute is responsible for burned area by PFT
    npft   = 'vegetation_class'                 # NetCDF attribute is responsible for PFT

    # 2.5: Additional settings (don't change).
    esa_datasets  = ['ESA-CCL'] * len(years)    # one data for one year
    param_var     = [nvar]      * len(years)    # one data for one year
    ndep_datasets = ['NDEP']
    ret_coef      = 1e9                         # return original units (in xrlib.get_data - is 1e-9)
    nat_pft = 3

    # -- Shell scripts for unzip and final post_processing:
    if lsets.get('lcluster'):
        prep_unzip = '../people/evchur/scripts/scripts_git/MPI-BGC/unzip_ESA.sh'
        shell_script = '../people/evchur/scripts/scripts_git/MPI-BGC/postprocess_ESA.sh'

    # =============================    Main program   ======================
    # -- Get input dataset paths and attributes (NDEP, MODIS):
    ndep_pin, ndep_param = get_path_in(['NDEP'], 'ndep', lsets)
    print(ndep_pin, '\n', ndep_param, '\n')
    path_esa, esa_param  = get_path_in(['BA_MODIS'], 'burned_area_year', lsets)
    print(path_esa, '\n', esa_param, '\n')
    # -- Unzip raw data:
    if (lzero and lsets.get('lcluster')):
        rc = subprocess.call(prep_unzip, shell=True)
        time.sleep(30)
        print('Done. ESA-CCI data were unpacked')
    # -- Get actual data paths for ESA-CCI and NDEP data:
    esa_pin = [f'{path_esa[0]}_{year}.nc' for year in years]
    esa_pout = [f'{data_out}ba_fraction_{year}.nc' for year in years]

    # -- Get actual ESA-CCI and NDEP data:
    ndep_data = get_data(
        ndep_pin, ndep_datasets, 'NDEP', 'ndep', tlm, lresmp = False )[0]
    esa_data  = get_data(
        esa_pin, esa_datasets, lparam, param_var, tlm, lresmp = False)

    # -- Upscalling burned area data from 0.25 to 0.5 grid resolution:
    ba_fraction = [] # burned area fraction by pft
    tot_ba025   = [] # total burned area (0.25 deg - resolution grid)
    tot_baf025  = [] # total burned area fraction (0.25 deg - resolution grid)
    tot_ba05    = [] # total burned area (0.5  deg - resolution grid)
    tot_baf05   = [] # total burned area fraction (0.5  deg - resolution grid)
    for i in range(len(esa_data)):
        print(f'Preprocessing data from {years[i]} year')

        # -- Convertation burned area to burned fraction and upscaling from 0.25 to 0.5 deg.
        ba_frac, tba025, tbaf025, tba05, tbaf05 = get_upscaling_ba_veg_class(
            esa_data[i], nvar, lreport = False, lplot = True)

        ba_frac = (ba_frac *  ret_coef) / comp_area_lat_lon(ba_frac.lat.values,
                                                            ba_frac.lon.values)
        # -- Re-interpolation ESA-CCI data to ndep grid (time ignore).
        #    NDEP has lat from -90 to 90, ESA from 90 to -90
        ba_frac = ba_frac.interp_like(ndep_data.drop_dims('time'), method = 'nearest')
        ba_fraction.append(ba_frac)
        # -- Get total burned area data and fractions for visualization:
        # Burned area and burned area fraction (grid - 0.25 deg)
        tot_ba025.append(tba025)
        tot_baf025.append(tbaf025)
        # Burned area and burned area fraction (grid - 0.50 deg)
        tot_ba05.append(tba05)
        tot_baf05.append(tbaf05)

    # -- Get monthly values of all natural PFT and save them into new NetCDF
    if nc_prep:
        for year in range(len(ba_fraction)):
            # -- Get total burned fraction of all natural PFT
            ntba_pft = ba_fraction[year][:, nat_pft:, :,:].sum(dim = {npft})
            # -- Rename attributes in output NetCDF file
            #    (Should be the same as OCN input data):
            current_indexes = ntba_pft.indexes
            desired_order = ['lon', 'lat', 'time']
            reordered_indexes = {index_name: current_indexes[index_name] for index_name in desired_order}
            ntba_pft = ntba_pft.reindex(reordered_indexes)
            # -- Settings for lat:
            ntba_pft.lat.attrs['standard_name'] = 'latitude'
            ntba_pft.lat.attrs['long_name']     = 'LATITUDE'
            ntba_pft.lat.attrs['units']         = 'degrees_north'
            ntba_pft.lat.attrs['axis']          = 'Y'
            ntba_pft.lat.encoding['_FillValue'] = None
            ntba_pft.lat.encoding['dtype']      = 'float32'
            # -- Settings for lon:
            ntba_pft.lon.attrs['standard_name'] = 'longitude'
            ntba_pft.lon.attrs['long_name']     = 'LONGITUDE'
            ntba_pft.lon.attrs['units']         = 'degrees_east'
            ntba_pft.lon.attrs['axis']          = 'X'
            ntba_pft.lon.encoding['_FillValue'] = None
            ntba_pft.lon.encoding['dtype']      = 'float32'
            # -- Settings for tot_ba_fraction:
            ntba_pft.name = 'tot_ba_fraction'
            ntba_pft.attrs['long_name']         = 'total_burned_area_fraction'
            ntba_pft.attrs['units']             = '0-1, unitless'
            ntba_pft.attrs['cell_methods']      = 'sum of natural ESA-CCI veg classes'
            ntba_pft.encoding['dtype']          = 'float32'
            # -- Save NetCDF file:
            ntba_pft.to_netcdf(esa_pout[year])

    # -- Visualization:
    if lplot:
        # -- Create comparison plots for burned area fraction on different grids (0.25 and 0.5):
        for year in range(len(years)):
            # Get relevant data
            ffrac_025 = (((esa_data[year][nvar] * ret_coef) / esa_data[year]['area'])
                           .sum(dim = npft))
            ffrac_05  = ba_fraction[year].sum(dim = npft)

            # -- Set new output paths for figures:
            user_map_settings['fire_025']['output'] = fig_out + f'baf_esa025_{years[year]}.png'
            user_map_settings['fire_050']['output'] = fig_out + f'baf_esa05_{years[year]}.png'
            # -- Plot 1: Fire fraction at 0.25 degree grid
            xrplot(ffrac_025, 'fire_025', user_map_settings)
            # -- Plot 2: Fire fraction at 0.5 degree grid
            xrplot(ffrac_05 , 'fire_050', user_map_settings)
            # -- Clean title:
            user_map_settings['fire_025']['output'] = ''
            user_map_settings['fire_050']['output'] = ''

        # -- Comparison annual values of burned area and burned area fraction
        #    on different grids (space resolutions - 0.25 and 0.5 degree)
        # Add new data to the list
        lst4data = [
            get_data_vis(tot_ba025 , 'ba'), get_data_vis(tot_baf025, 'baf'),
            get_data_vis(tot_ba05  , 'ba'), get_data_vis(tot_baf05 , 'baf'),
        ]
        # Plot 3: Linear plot for annual values (2-axis: 1 - burned area; 2 - fraction)
        lplot2axis(lst4data, user_line_settings)

    # -- Run final postprocessing script:
    # Add land/water mask + Set missing values and calendar type
    if lsets.get('lcluster'):
        rc = subprocess.call(shell_script, shell = True)
        time.sleep(15)
        print('Done. ESA-CCI data were processed')
# ============================== Program END  =========================
