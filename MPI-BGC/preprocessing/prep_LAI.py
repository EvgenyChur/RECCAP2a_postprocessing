# -*- coding: utf-8 -*-
"""
There are a lot of LAI datasets in NetCDF format. Each of them has unique key 
attributes, grid resolution, time steps that can be a problem for dataprocessing. 
In particular, the model code can be too difficult for understanding if all these
settings will be implemented in it. Because of that, we decided to create a 
special script for preprocessing LAI data based on different datasets.

Actual LAI datasets:
    1. LTDR;
    2. MODIS;
    3. GLOBMAP

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-08-15 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
    1.2    2022-10-25 Evgenii Churiulin, MPI-BGC
           Updating full structure of the script
    1.3    2022-11-11 Evgenii Churiulin, MPI-BGC
           Add new enviroments, paths for figures
"""

# =============================== Import modules =======================
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import subprocess
import time
import warnings
warnings.filterwarnings("ignore")
from settings import logical_settings, get_settings4domains, config
from libraries import makefolder

# =============================== User functions =======================

# -- get_paths --> get actual path to the LAI datasets
def get_paths(
        # Input variables:
        main:str,                       # Common path for all datasets
        dataset:str,                    # Name of the actual dataset
        grid_settings:dict,             # Settings for the actual dataset (grid domain, time period)
        lcluster:bool,                  # Do you want to work on the cluster?
        # Output variables:
    ) -> tuple[str, str, str]:          # Input path, Output path for data and
                                        #             Output path for figures
    # -- Local variables:
    grid_in  = grid_settings.get(dataset)[0]
    grid_out = grid_settings.get(dataset)[1]
    fst_yr   = grid_settings.get(dataset)[2]
    lst_yr   = grid_settings.get(dataset)[3]

    # -- Define output path:
    if lcluster:
        main_in  = main  + '/data/DataStructureMDI/DATA/grid/Global'
        main_out = main  + '/scratch/evchur/LAI'
        # Datasets paths (except OCN simulations): 
        catalog = {
            'LTDR' : {
                'pin'     : main_out + f'/LAI_0d05_annual/LAI.{grid_in}',
                'pout'    : main_out + f'/LTDR_LAI_{grid_out}_annual/LTDR_LAI.{grid_out}',
                'dif_pout': main_out + f'/LTDR_LAI_{grid_out}_annual/LTDR_LAI.{grid_out}.{fst_yr}_{lst_yr}_annual.nc',
            },
            'MODIS' : {
                'pin'     : main_in  + f'/0d50_monthly/MODIS/MOD15A2H.006/Data/Lai/Lai_average.{grid_in}',
                'pout'    : main_out + f'/MODIS_LAI_{grid_out}_monthly/MODIS_LAI.{grid_out}',
                'dif_pout': main_out + f'/MODIS_LAI_{grid_out}_monthly/MODIS_LAI.{grid_out}.{fst_yr}_{lst_yr}.nc',
            },
            'GLOBMAP' : {
                'pin'     : main_in  +  '/0d50_monthly/globmap_LAI/v3/Data/GLOBMAP_LAI.monthly',
                'pout'    : main_out + f'/GLOBMAP_LAI_{grid_out}_monthly/GLOBMAP_LAI.{grid_out}',
                'dif_pout': main_out + f'/GLOBMAP_LAI_{grid_out}_monthly/GLOBMAP_LAI.{grid_out}.{fst_yr}_{lst_yr}.nc',
            }
        }
    else:
        # Datasets paths (except OCN simulations):  
        catalog = {
            'LTDR' : {
                'pin'     : main + f'/LTDR_LAI_{grid_in}_annual/LAI.{grid_in}',
                'pout'    : main + f'/LTDR_LAI_{grid_out}_annual/LTDR_LAI.{grid_out}',
                'dif_pout': main + f'/LTDR_LAI_{grid_out}_annual/LTDR_LAI.{grid_out}.{fst_yr}_{lst_yr}_annual.nc',
            },
            'MODIS' : {
                'pin'     : main + f'/MODIS_LAI_{grid_in}_monthly/Lai_average.{grid_in}',
                'pout'    : main + f'/MODIS_LAI_{grid_out}_monthly/MODIS_LAI.{grid_out}',
                'dif_pout': main + f'/MODIS_LAI_{grid_out}_monthly/MODIS_LAI.{grid_out}.{fst_yr}_{lst_yr}.nc',
            },
            'GLOBMAP' : {
                'pin'     : main + f'/GLOBMAP_LAI_{grid_in}_monthly/GLOBMAP_LAI.monthly',
                'pout'    : main + f'/GLOBMAP_LAI_{grid_out}_monthly/GLOBMAP_LAI.{grid_out}',
                'dif_pout': main + f'/GLOBMAP_LAI_{grid_out}_monthly/GLOBMAP_LAI.{grid_out}.{fst_yr}_{lst_yr}.nc',
            }
        }
    # -- Get actual data paths for datasets (pin, pout, pout_diff):
    path_in = catalog.get(dataset).get('pin')
    path_out = catalog.get(dataset).get('pout')
    dpath_out = catalog.get(dataset).get('dif_pout')
    return path_in, path_out, dpath_out

# -- prep_data --> Rename key attributes of NetCDF files and re-interpolation
#                  of them to OCN regular grid (720*300)
def prep_data(
        # Input variables:
        refer:xr.DataArray,        # OCN simulation. Script uses this dataset as reference (lat, lon). Time ignore
        data_in:str,               # Path to input data.
        data_out:str,              # Path for output data.
        fst_year:str,              # First year.
        lst_year:str,              # Last year.
        period:str,                # Additional prefix in data.
        mode:str,                  # Version of the LAI dataset.
        uconfig:config,            # User class with settings
        # Output variables:
    ) -> xr.DataArray:             # LAI dataset re-interpolated to OCN grid
    # -- Load domains:
    domain_lim = get_settings4domains(uconfig)

    # -- Select all available years from the folder:
    years = np.arange(fst_year, lst_year + 1, 1)
    # -- Get name for output file (full series):
    if mode == 'LTDR':
        pout_period = f'{data_out}.{years[0]}_{years[-1]}_{period}.nc'
    else:
        pout_period = f'{data_out}.{years[0]}_{years[-1]}.nc'
    # -- Get LAI values:
    lst4lai = []
    for year in years:
        if mode == 'LTDR':
            pin  = f'{data_in}.{year}_{period}.nc'
            pout = f'{data_out}.{year}_{period}.nc'
        else:
            pin  = f'{data_in}.{year}.nc'
            pout = f'{data_out}.{year}.nc'
        # -- Open dataset:
        ds = xr.open_dataset(pin)
        # -- Rename attributes:
        if  mode == 'LTDR'  :
            ds = ds.rename({'longitude':'lon', 'latitude':'lat', 'LAI':'lai'})
        elif mode == 'MODIS':  
            ds = ds.rename({ 'Lai_average' : 'lai'})
        else:
            ds = ds.rename({ 'GLOBMAP_LAI' : 'lai'})
        # -- Select area (OCN grid: lon 180E - 180W; lat 90N - 60S):
        ds = ds.sel(
            lat = slice(domain_lim.get(region)[0], domain_lim.get(region)[1]),
            lon = slice(domain_lim.get(region)[2], domain_lim.get(region)[3])
        )
        # -- Re-interpolation on OCN grid:
        ds = ds.interp_like(refer.drop_dims('time'), method = 'nearest')
        # -- Add to list and save file:
        lst4lai.append(ds)
        ds.to_netcdf(pout)
    # -- Get and save a full set:
    lai_period = xr.concat(lst4lai, dim = 'time')
    lai_period.to_netcdf(pout_period)
    return(lai_period)

# data4diff --> get timemean values for LAI parameter of current dataset:
def data4diff(pin:str, time_limits:list[int]) -> xr.DataArray:
    # -- Local variables:
    var = 'lai'
    var4mean = 'time'
    # -- Open datasets:
    ds_lai = xr.open_dataset(pin)
    # -- Select the same time range:
    ds_lai = ds_lai.sel(time = slice(f'{time_limits[0]}', f'{time_limits[1]}'))
    # Get mean values:
    ds_mean = ds_lai[var].mean([var4mean])
    return ds_mean

# -- get_plot --> Create a simple plot for understanding:
#                 a. annual LAI values based on the actual dataset
#                 b. collage plot with monthly LAI values
def get_plot(
        # Input variables:
        data:xr.DataArray,              # data for visualization
        yr1:int,                        # first year
        yr2:int,                        # last year
        data_out:str,                   # output path
        mode:str,                       # type of plot (collage or mean)
        # Output variables:
    ):                                  # Create figure in output folder
    # -- Start visualization:
    fig = plt.figure(figsize = (12,7))
    if mode == 'collage':
        (data.sel(time  = slice(yr1, yr2))
             .plot(col  = 'time', col_wrap = 5, robust = True, cmap = 'Greens', 
                   vmin = 0     , vmax     = 6))
        fig_out = f'{data_out}_{yr1}_{yr2}.png'
    else:
        data.mean(['time']).plot(robust = True, cmap = 'Greens', vmin = 0, vmax = 6)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Mean LAI from {yr1} - {yr2}')
        fig_out = f'{data_out}_mean_{yr1}_{yr2}.png'

    plt.savefig(fig_out, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()


if __name__ == '__main__':
    # ============================= Users settings ========================
    # -- Load basic logical settings:
    lsets = logical_settings(lcluster = True, lnc_info = False)
    # Do you want to work on cluster?
    lcluster = lsets.get('lcluster')
    # Do you want to get annual LTDR data from daily?
    lLTDR_annual = False
    # Preprocessing of LTDR data?
    lproc_ltdr = True
    # Preprocessing of MODIS data?
    lproc_modis = True
    # Preprocessing of GLOBMAP data?
    lproc_globmap = True
    # Do you want to compare datasets and get collage plot?
    ldiff = True

    # -- Load basic user settings:
    bcc = config.Bulder_config_class()
    tlm = bcc.user_settings()

    # -- Define actual data paths
    # Research domain:
    region  = 'Global'
    #                 Dataset     input grid   output grid   Available years
    #                              (size)        (size)        first    last
    grid_settings = {'LTDR'    : ['7200.3600', '720.300'   ,   1981,    2020],
                     'MODIS'   : [ '720.360' , '720.300'   ,   2000,    2020],
                     'GLOBMAP' : [ '720.360' , '720.300'   ,   1982,    2020]}

    if lcluster:
        main = '..I'
        # OCN datasets:
        ocn_in = f'{main}/work_1/RECCAP2/NRT/OCNout/Fire/OCN_S2.1_lai.nc'
        # Output:
        diff_out = f'{main}/scratch/evchur/LAI/collage_lai_diff.png'
    else:
        main = 'C:/Users/evchur/Desktop/DATA/LAI'
        ocn_in = f'{main[0:-4]}/OCN_fire/RECCAP_DATA/OCN_S2.1_lai.nc'
        diff_out = f'{main}/collage_lai_diff.png'

    # -- Define settings for collage plot:
    if ldiff:
        tlim = [2001, 2020]
        # Settings for colage plot
        clr = 'black'
        fsize = 14.0
        lpab = 20.0
        vmin_lim = 0.0
        vmax_lim = 6.0
        diff_lim = 0.6
        # Plot titles for the plot
        plot_titles = ['LTDR', 'MODIS'  , 'DIFF (LTDR - MODIS)'  ,
                       'LTDR', 'GLOBMAP', 'DIFF (LTDR - GLOBMAP)']
        # y and x labels:
        ylabels = ['Latitude', '','', 'Latitude' , '', '']
        xlabels = ['', '', '', 'Longitude', 'Longitude', 'Longitude']

    # -- Additional settings:
    ftime_plot  = "2000" # time filter for plots (from fst_yr      to ftime_plot)
    ftime_plot2 = "2001" # time filter for plots (from ftime_plot2 to lst_yr    )

    shell_script = '../people/evchur/scripts/scripts_git/MPI-BGC/preprocessing/yearmean_lai.sh'

    # =============================    Main program   =======================
    # -- Get input paths:
    ltdr_in, ltdr_out, ltdr_lai_path = get_paths(
        main, 'LTDR', grid_settings, lcluster)
    modis_in, modis_out, modis_lai_path = get_paths(
        main, 'MODIS', grid_settings, lcluster)
    globmap_in, globmap_out, globmap_lai_path = get_paths(
        main, 'GLOBMAP', grid_settings, lcluster)

    # -- Get annual values for LTDR dataset based on daily values:
    if (lLTDR_annual is True and lcluster is True):
        rc = subprocess.call(shell_script, shell = True)
        time.sleep(1400)

    # -- Get OCN data with reference grid:
    ds_ocn  = (
        xr.open_dataset(ocn_in, decode_times = False)
          .assign_coords({'time' : pd.date_range("1950-01-01", "2022-01-01", freq = "M")})
          .sel(time=slice('1980','2020'))
    )

    # -- Get LTDR data:
    if lproc_ltdr:
        dataset = 'LTDR'
        fst_yr  = grid_settings.get(dataset)[2]
        lst_yr  = grid_settings.get(dataset)[3]
        step    = 'annual'
        # Get LTDR data and save them into NetCDF:
        mean_ltdr  = prep_data(
            ds_ocn, ltdr_in, ltdr_out, fst_yr, lst_yr, step, dataset, tlm)
        # Get LTDR plot:
        get_plot(mean_ltdr['lai'], f"{fst_yr}", ftime_plot , ltdr_out, 'collage')
        get_plot(mean_ltdr['lai'], ftime_plot2, f'{lst_yr}', ltdr_out, 'collage')
        get_plot(mean_ltdr['lai'], f'{fst_yr}', f'{lst_yr}', ltdr_out, 'mean')

    # -- Get MODIS data:
    if lproc_modis:
        dataset  = 'MODIS'
        fst_yr   = grid_settings.get(dataset)[2]
        lst_yr   = grid_settings.get(dataset)[3]
        step     = 'monthly'
        # -- Get MODIS data and save them into NetCDF
        modis_lai  = prep_data(
            ds_ocn, modis_in, modis_out, fst_yr, lst_yr, step, dataset, tlm)
        # -- Get MODIS plot
        mean_mod = modis_lai.resample(time = 'A').mean('time')
        get_plot(mean_mod['lai'], f'{fst_yr}', f'{lst_yr}', modis_out, 'collage')
        get_plot(mean_mod['lai'], f'{fst_yr}', f'{lst_yr}', modis_out, 'mean')

    # -- Get GLOBMAP data:
    if lproc_globmap:
        dataset = 'GLOBMAP'
        fst_yr  = grid_settings.get(dataset)[2]
        lst_yr  = grid_settings.get(dataset)[3]
        step    = 'monthly'
        # Get GLOBMAP data and save them into NetCDF
        globmap_lai = prep_data(
            ds_ocn, globmap_in, globmap_out, fst_yr, lst_yr, step, dataset, tlm)
        # Get GLOBMAP plot:
        mean_glb = globmap_lai.resample(time = 'A').mean('time')
        get_plot(mean_glb['lai'], f'{fst_yr}', ftime_plot , globmap_out, 'collage')
        get_plot(mean_glb['lai'], ftime_plot2, f'{lst_yr}', globmap_out, 'collage')
        get_plot(mean_glb['lai'], f'{fst_yr}', f'{lst_yr}', globmap_out, 'mean')

    # -- Create collage for LAI difference:
    if ldiff:
        # -- Get data from datasets:
        ltdr_mean = data4diff(ltdr_lai_path, tlim)
        modis_mean = data4diff(modis_lai_path, tlim)
        globmap_mean = data4diff(globmap_lai_path, tlim)

        # -- Get difference (LTDR - MODIS or GLOBMAP):
        diff_lm = ltdr_mean - modis_mean
        diff_lg = ltdr_mean - globmap_mean

        # -- Create plots and prepare data for that:
        lst4lai = [ltdr_mean, modis_mean  , diff_lm,
                   ltdr_mean, globmap_mean, diff_lg]

        # -- Get fast LAI difference view:
        fig = plt.figure(figsize = (14,10))
        # Create grid
        egrid = (2, 3)
        ax_list = []
        for i in range(egrid[0]):
            for j in range(egrid[1]):
                ax_list.append(plt.subplot2grid(egrid, (i, j), rowspan = 1, colspan = 1))
        # Get plots
        for i in range(len(lst4lai)):
            if i not in (2, 5):
                lst4lai[i].plot(
                    robust = True,
                    cmap = 'Greens',
                    vmin = vmin_lim,
                    vmax = vmax_lim,
                    ax = ax_list[i],
                )
            else:
                lst4lai[i].plot(
                    robust = True,
                    cmap = 'PiYG',
                    vmin = -1.0 * diff_lim,
                    vmax = diff_lim,
                    ax = ax_list[i],
                )
            ax_list[i].set_title(f'{plot_titles[i]}', color = clr, fontsize = fsize, pad = lpab)
            ax_list[i].set_ylabel(f'{ylabels[i]}', color = clr, fontsize = fsize, labelpad = lpab)
            ax_list[i].set_xlabel(f'{xlabels[i]}', color = clr, fontsize = fsize, labelpad = lpab)
        plt.tight_layout()
        plt.savefig(diff_out, format = 'png', dpi = 300)
        plt.close(fig)
        plt.gcf().clear()
    print('END program')
    # ============================== Program END  =========================
