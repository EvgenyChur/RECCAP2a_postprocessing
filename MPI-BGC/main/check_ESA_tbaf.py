# -*- coding: utf-8 -*-
"""
The main purpose of this script is calculation of differences between natural total 
annual burned area fraction (tbaf) calculated based on ESA-CCI MODIS data and total
annual land cover fraction (tland) calculated based on OCN natural PFT. 

All values of tbaf should be lower then tland. Otherwise, it means that we have 
more burned area fraction that the OCN model has and it is not correct.

Also, script is able to visualize output data. 

Information about OCN PFT:
    pft  1: '          bared ground            ', 'natural'
    pft  2: 'tropical  broad-leaved evergreen  ', 'natural'
    pft  3: 'tropical  broad-leaved raingreen  ', 'natural'
    pft  4: 'temperate needleleaf   evergreen  ', 'natural'
    pft  5: 'temperate broad-leaved evergreen  ', 'natural'
    pft  6: 'temperate broad-leaved summergreen', 'natural'
    pft  7: 'boreal    needleleaf   evergreen  ', 'natural'
    pft  8: 'boreal    broad-leaved summergreen', 'natural'
    pft  9: 'boreal    needleleaf   summergreen', 'natural'
    pft 10: '          C3           grass      ', 'natural'
    pft 11: '          C4           grass      ', 'natural'
    pft 12: '          C3           agriculture', ' crops '
    pft 13: '          C4           agriculture', ' crops '

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-09-09 Evgenii Churiulin, MPI-BGC
           Initial release;
    1.2    2022-10-24 Evgenii Churiulin, MPI-BGC
           Update script structure and change script according to the changes in
           xarray_lib module;
    1.3    2022-11-14 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.4    2023-05-23 Evgenii Churiulin, MPI-BGC
           Code refactoring + relocated function for visualization NetCDF data to
           lib4visualization as create_fast_xarray_plot
    1.5    2023-11-13 Evgenii Churiulin, MPI-BGC
           Small updates in user settings
"""
# =============================== Import modules ========================
# -- Standard modules
import os
import sys
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# -- Personal modules
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings import logical_settings, config, get_path_in, get_output_path
from libraries import makefolder
from libraries import create_fast_xarray_plot as xrplot

# =============================   Personal functions   ==================

def get_data(lst4paths:list[str]) -> list[xr.Dataset]:
    """Reading input NetCDF data
        **Input variables:**
        lst4paths - Input data paths

        **Output variables:**
        Dataset - Datasets with research information
    """
    # -- Read NetCDF data and add them to output list:
    return [xr.open_dataset(path) for path in lst4paths]

if __name__ == '__main__':

    # ============================= Users settings =========================
    # -- Load basic logical settings:
    lsets = logical_settings(lcluster = True, lnc_info = False)
    # -- Load other logical parameters:
    lsim_plot = True # Do you want to create plots?
    # -- Load basic user settings:
    bcc = config.Bulder_config_class()
    tlm = bcc.user_settings()

    # -- Select available years for ESA-CCI data:
    years = np.arange(2001, 2021, 1)
    #years = np.arange(2001, 2002, 1)

    # -- Create relevant OUTPUT folder for script results:
    path_out  = makefolder(get_output_path(lsets).get('check_ESA_tbaf'))
    print(f'Your data will be saved at {path_out}')

    # -- Settings for 2D maps:
    plt_settings = {
        'all_PFT' : {
            'robust'   : True,
            'colormap' : 'terrain_r',
            'vmin'     : 0.0,
            'vmax'     : 1.0,
            'col'      : None,
            'col_wrap' : None,
            'title'    : 'Land fraction from all OCN PFTs',
            'output'   : path_out + 'lfrac_all_PFT.png',
        },
        'nat_PFT' : {
            'robust'   : True,
            'colormap' : 'terrain_r',
            'vmin'     : 0.0,
            'vmax'     : 1.0,
            'col'      : None,
            'col_wrap' : None,
            'title'    : 'Land fraction from natural OCN PFTs',
            'output'   : path_out + 'lfrac_nat_PFT.png',
        },
        'diff_PFT' : {
            'robust'   : True,
            'colormap' : 'PRGn',
            'vmin'     : -1.0,
            'vmax'     :  1.0,
            'col'      : None,
            'col_wrap' : None,
            'title'    : 'Land fraction difference between all and natural PFT',
            'output'   : path_out + 'lfrac_diff.png',
        },
        'annual_diff' : {
            'robust'   : True,
            'colormap' : 'PRGn',
            'vmin'     : -0.2,
            'vmax'     :  0.2,
            'col'      : None,
            'col_wrap' : None,
            'title'    : '',
            'output'   : '',
        },
        'monthly_diff' : {
            'robust'   : True,
            'colormap' : 'PRGn',
            'vmin'     : -0.2,
            'vmax'     :  0.2,
            'col'      : 'time',
            'col_wrap' : 4,
            'output'   : '',
        },
    }

    # -- Settings for histogram:
    hist_settings = {
        'fsize': 16.0,
        'lpad' : 20.0,
        'clr'  : 'k',
        'x_rotation' : 0.0,
        #         min   max   step
        'xlim' : [2000, 2022,  2.0],
        'ylim' : [0.0, 160.0, 20.0],
        'title' : 'Number of bad points \n (ESA-CCI burned fraction > OCN land cover fraction)',
        'xlable' : 'Years',
        'ylabel' : 'Numbers of points',
        'hist_out' : path_out + 'bad_points.png',
    }


    # ==============================  Main program  ========================
    print('START program')
    # -- Get relevant INPUT data paths:
    #    P.S.: function get_path_in return 2 parameters, but we didn't use the
    #          second output parameter (land_param and fire_param) in this script
    #    P.S.: Data presented on grid with resolution (360*720) and ESA-CCI MODIS
    #          dataset was preprocessed before this step:
    land_pin, land_param = get_path_in(['LANDCOVER'], 'landuse_2010', lsets)
    path_fire, fire_param = get_path_in(['BA_MODIS'], 'burned_area_post', lsets)
    # -- Get correct input paths for preprocessed ESA-CCI MODISv5.0 dataset depending
    #    on actual year:
    fire_pin = [path_fire[0] + f'_{year}.nc' for year in years ]
    # -- Reading input data:
    #    In case of landcover, data we are using the same landcover map (landcover_2010)
    #    for all years. Because of that we have to use only the first landcover dataset
    fire_data = get_data(fire_pin)
    land_data = get_data(land_pin)[0]
    # -- Get actual values of land fraction for all PFT and only natural PFT (1:11):
    tland_all = land_data['maxvegetfrac'].sum(dim = {'veget'})
    tland_nat = land_data['maxvegetfrac'][:,1:11,:,:].sum(dim = {'veget'})
    # -- Create plots:
    if lsim_plot:
        # -- Land fraction from all OCN PFT:
        xrplot(tland_all, 'all_PFT', plt_settings)
        # -- Land fraction based on natural OCN PFT:
        xrplot(tland_nat, 'nat_PFT', plt_settings)
        # -- Difference between all PFT and natural PFT:
        xrplot(tland_all - tland_nat, 'diff_PFT', plt_settings)
    # -- Fire fraction data
    bad_points = []
    for year in range(len(years)):
        # -- Get total annual burned area fraction:
        tot_baf = fire_data[year]['tot_ba_fraction'].sum(dim = 'time')
        # -- Get number of points where (tot_baf - tland_nat) > 0. It means that
        #    we burn more fraction that we have in that point. Ideal option bad_point = 0,
        #    however, we have several bad_points:
        bad_points.append(np.count_nonzero((tot_baf - tland_nat)[:,:,0].data > 0.0))
        # -- Get total monthly burned area fraction difference:
        one_month = []
        for month in range(len(fire_data[year].time)):
            one_month.append(fire_data[year]['tot_ba_fraction'][month] - (tland_nat / 12))
        one_year = xr.concat(one_month, dim = 'time')

        # -- Create plots for comparison:
        if lsim_plot:
            # -- Set new title and outputs for figures:
            plt_settings['annual_diff']['title'] = (
                'Difference between annual burned area and land cover '
                f'fractions in {years[year]} yr.')
            plt_settings['annual_diff']['output'] = (
                path_out + f'annual_fdiff_{years[year]}.png')
            plt_settings['monthly_diff']['output'] = (
                path_out + f'monthly_fdiff_{years[year]}.png')
            # -- Difference between annual fire fraction - land fraction:
            xrplot(tot_baf - tland_nat, 'annual_diff', plt_settings)
            # -- Monthly difference between annual fire fraction - land fraction:
            xrplot(one_year, 'monthly_diff', plt_settings)
            # -- Clean title:
            plt_settings['annual_diff']['title'] = ''
            plt_settings['annual_diff']['output'] = ''
            plt_settings['monthly_diff']['output'] = ''

    # -- Create histogram with bad point numbers in each research year:
    sbad_points = pd.Series(bad_points, index = years)
    # -- Use user settings for historgram:
    clr =  hist_settings.get('clr')
    fsize = hist_settings.get('fsize')
    lpab = hist_settings.get('lpad')

    # -- Create figure:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(
        sbad_points.index,
        sbad_points,
        width = 1,
        edgecolor = "white",
        linewidth = 0.7,
    )
    # -- Plot settings (Limits, titles, fonts):
    ax.set(
        xlim = (hist_settings.get('xlim')[0], hist_settings.get('xlim')[1]),
        xticks = np.arange(
            hist_settings.get('xlim')[0],
            hist_settings.get('xlim')[1],
            hist_settings.get('xlim')[2],
        ),
        ylim = (hist_settings.get('ylim')[0], hist_settings.get('ylim')[1]),
        yticks = np.arange(
            hist_settings.get('ylim')[0],
            hist_settings.get('ylim')[1] + 0.1,
            hist_settings.get('ylim')[2],
        ),
    )
    ax.set_title(
        hist_settings.get('title'),
        color = clr,
        fontsize = fsize,
        pad = lpab,
    )
    ax.set_xlabel(
        hist_settings.get('xlable'),
        color = clr,
        fontsize = fsize,
        labelpad = lpab,
    )
    ax.set_ylabel(
        hist_settings.get('ylabel'),
        color = clr,
        fontsize = fsize,
        labelpad = lpab,
    )
    # -- Set size and position of x and y values (ticks)
    for label in ax.xaxis.get_ticklabels():
        label.set_color(clr)
        label.set_rotation(hist_settings.get('x_rotation'))
        label.set_fontsize(fsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_color(clr)
        label.set_fontsize(fsize)
    # -- Add plot grid:
    plt.grid(
        True,
        which = 'major',
        color = 'grey',
        linestyle = 'dashed',
        alpha = 0.2,
    )
    # -- Save figure and clean memory:
    plt.savefig(hist_settings.get('hist_out'), format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()
    print('END program')
# ============================== Program END  ============================
