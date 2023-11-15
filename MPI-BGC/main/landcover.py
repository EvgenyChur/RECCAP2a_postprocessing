# -*- coding: utf-8 -*-
"""
Script for processing of landcover fraction by PFT:
    1. Calculating and visualisation of burned area difference (GFED - OCN) by PFT
    2. Calculating and visualisation of PFT fraction for random points (stations)

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de


History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-08-18 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-28 Evgenii Churiulin, MPI-BGC
           Updating script structure and adapting all functions to the new versions
           of personal modules
    1.3    2022-11-04 Evgenii Churiulin, MPI-BGC
           Added new dataset for comparison ESA-CCI MODIS and modified the script
           for fast chaning the datasets 
    1.4    2022-11-15 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.5    2023-05-31 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
#=============================     Import modules     =========================
# -- Standard modules:
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
# -- Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings import (logical_settings, config, get_path_in, get_output_path,
    get_settings4ds_time_limits, get_settings4stations, get_ocn_pft,
    get_settings4plots_landcover)
from libraries import (makefolder, get_data, get_interpol, plot_diff_hist,
    tick_rotation_size)
# =============================   Personal functions   =================
def read_data(region:str, lst4datasets:list[str], var:str, lsettings:bool,
        lresmp:bool, uconfig:config) -> tuple[list[xr.Dataset]]:
    """Get data presented on OCN grid for your research parameter

    **Input variables:**
        region - Research domain (Global, Europe, Other..)
        lst4datasets - Research datasets for analysis
        var - Research parameter (nc - attrubite)
        lsettings - logical settings
        lresmp - Do you want to use time resample algorithm?
        uconfig - User class with settings

    **Output variables:**
        lst4data - Research data presented on OCN grid
    """
    # -- Get information about datasets:
    lmodis_nat = True
    # -- Get absolute data paths
    ipaths, res_param = get_path_in(lst4datasets, var, lsettings)
    if lmodis_nat:
        for i in range(len(lst4datasets)):
            if lst4datasets[i] == 'BA_MODIS':
                tmp_ipath, tmp_res_param = get_path_in(['BA_MODIS'], 'burned_area_nat', lsettings)
                ipaths[i] = tmp_ipath[0]
                res_param[i] = tmp_res_param[0]
    # -- Read in data:
    lst4data = get_data(
        ipaths,
        lst4datasets,
        var,
        res_param,
        uconfig,
        linfo = lsettings.get('lnc_info'),
        lresmp = lresmp,
    )
    # -- Convert data to one grid size:
    if var == 'burned_area':
        lst4data = get_interpol(lst4data, lst4datasets, region, var, uconfig)
    return lst4data


if __name__ == '__main__':
    # ================   User settings (have to be adapted)  ==============
    # -- Load basic logical settings:
    lsets = logical_settings(lcluster = True, station_mode = True)
    # -- Load other logical parameters:
    linfo = lsets.get('lnc_info')         # Do you want to get more information about data?
    lstations = lsets.get('station_mode') # Do you want to get data for PFT at stations?
    lba_hist = True                       # Do you want to plot histogram of BA difference by PFT?

    # -- Load basic user settings:
    bcc = config.Bulder_config_class(ocn = [2003, 2020], modis = [2003,2020])
    tlm = bcc.user_settings()
    # -- Load user settings:
    stations = get_settings4stations(tlm)
    ocn_pft = get_ocn_pft(tlm)
    ln_colors = get_settings4plots_landcover(tlm)
    colors_ocn = [ln_colors.get('OCN').get(item['PFT'])[0] for item in ocn_pft]
    styles_ocn = [ln_colors.get('OCN').get(item['PFT'])[1] for item in ocn_pft]

    # -- Select research datasets, research parameters and domain:
    region = 'Global'          # Research region ('Global', Europe, NH, Tropics)
    refer = 'BA_MODIS'         # Select your reference dataset  ('BA_MODIS', 'GFED4.1s')
    param_BA = 'burned_area'   # Research parameter
    param_LC = 'landCoverFrac' # Name of land cover parameter

    # -- Get names of the research datasets with burned area and land cover:
    # Options: OCN_S2.1, _S2.2, _S3.1, _S3.2, _S2Prog, _S2Diag
    lst4ba_ds = ['OCN_S2Prog_v4', 'OCN_S2Diag_v4']  + [refer]
    lst4lc_ds = lst4ba_ds[:-1]

    # -- Define time period (Data have to have the same time periods
    #     GFED - 1997 to 2016; MODIS - 2001 - 2020; optimal 2001 - 2016
    t_start = get_settings4ds_time_limits(tlm).get(param_BA).get('OCN')[0]
    t_stop = get_settings4ds_time_limits(tlm).get(param_BA).get('OCN')[1]

    # -- Settings for collage plot:
    if lstations == True:
        rows      =   4   # row numbers
        cols      =   5   # column numbers
        ymin_pft  =   0.0 # y min
        ymax_pft  = 100.1 # y max
        ystep_pft =  10.0 # y step
        fsize     =  10.0 # text fontsize
        deg       =  90.0 # angle of x axis labels

    # ============================    Main program   ========================
    print('START program')
    # -- Define output paths and create folder for results:
    data_OUT = makefolder(get_output_path(lsets).get('landcover'))
    print(f'Your data will be saved at {data_OUT}')

    # -- Get burned area and land cover data (12 PFT + Bare soil in OCN simulation)
    lst4veget = read_data(region, lst4lc_ds, param_LC, lsets, False, tlm)
    lst4ba    = read_data(region, lst4ba_ds, param_BA, lsets, True, tlm)

    # -- Get actual PFT data:
    pft4simulations = []           # full list of PFT data
    for j in range(len(lst4lc_ds)):
        landCover = (lst4veget[j][param_LC]
                        .sel(time = slice(f'{t_start}', f'{t_stop}'))
                        .resample(time = 'A').mean('time'))
        # -- Get PFT values:
        veg_type  = landCover.vegtype.values
        # -- Get actual data for each OCN PFT in simulation:
        pft_data  = [landCover[:, i, :, :] for i in range(len(veg_type))]
        pft4simulations.append(pft_data)

    # -- Get actual PFT names:
    pft_sname = [] # short name of PFTs in OCN simulations (they are the same)
    for i in range(len(veg_type)):
        for item in ocn_pft:
            if (item['veg_type'] == veg_type[i]):
                pft_sname.append(item['PFT'])

    # -- PFT analysis for each station (table + figure):
    if lstations:
        print('Working on collage plot and data for stations \n')
        # -- Get actual PFT data for each station
        pft4datasets = []
        for j in range(len(lst4lc_ds)):
            pft4stations = [] # PFT for all stations
            nam_stations = [] # station names
            for st in range(len(stations)):
                # Get name of each station:
                nam_stations.append(stations.get(st + 1)[2])
                # Get latitude and longitude for each station:
                lats, lons = stations.get(st + 1)[0], stations.get(st + 1)[1]
                # Get PFT for each station:
                pft4station = [
                    pft4simulations[j][i].sel(lat = lats, lon = lons, method = 'nearest')
                    for i in range(len(pft4simulations[j]))]
                # -- Collect stations from one dataset:
                pft4stations.append(pft4station)
            # -- Collect datasets:
            pft4datasets.append(pft4stations)

        # -- Get PFT table for stations:
        for j in range(len(lst4lc_ds)):
            pft_dataset = []
            for st in range(len(stations)):
                pft_station = []
                for i in range(len(pft4datasets[j][st])):
                    pft_station.append(
                        pd.concat(
                            [
                                pd.Series(nam_stations[st]),
                                pd.Series(pft_sname[i]),
                                pd.Series(pft4datasets[j][st][i].mean('time').data * 100)  # get PFT values  in %
                            ], axis = 1
                        )
                    )
                # Collect pft's for one station:
                pft_dataset.append(pd.concat(pft_station, axis = 0 ))
            # Collect all stations:
            df_pft_all = pd.concat(pft_dataset, axis = 1 )
            # -- Rename columns and save file:
            df_pft_all = (
                df_pft_all.rename(columns = {0:'site', 1:'pft', 2:'data'})
                          .reset_index(drop = True)
            )
            df_pft_all.to_csv(
                data_OUT + f'{lst4lc_ds[j]}_PFT.csv',
                float_format = '%.3f',
                sep = ';',
                index = True,
            )

        # -- Create PFT plot for stations:
        for j in range(len(lst4lc_ds)):
            # -- Get grid
            fig = plt.figure(figsize = (14,10))
            egrid = (rows, cols)
            ax_list = []
            for act_row in range(egrid[0]):                                        # cycle by rows
                for act_col in range(egrid[1]):                                    # cycle by columns
                    ax_list.append(plt.subplot2grid(egrid, (act_row, act_col),
                                                    rowspan = 1, colspan = 1))

            for st in range(len(stations)):
                for i in range(len(pft4datasets[j][st])):
                    ax_list[st].plot(pft4datasets[j][st][i].time        ,
                                     pft4datasets[j][st][i].values * 100,          # PFT values in %
                                     label     = pft_sname[i]  ,
                                     linestyle = styles_ocn[i] ,
                                     color     = colors_ocn[i] )

                # Settings for each subplot
                ax_list[st].set_title(
                    f'{nam_stations[st]}', color = 'red', fontsize = fsize, pad = 7)   # Set title
                ax_list[st].set_yticks(np.arange(ymin_pft, ymax_pft, ystep_pft))       # Set y limits
                tick_rotation_size(ax_list[st], deg, fsize)                        # Set size and rotation for x and y axis
                # -- Grid settings:
                ax_list[st].grid(
                    True,
                    which = 'major',
                    color = 'grey',
                    alpha = 0.2,
                    linestyle = ':',
                )
                # -- Ignore subplots with index biger than:
                if st <= 11:
                    plt.setp(ax_list[st].get_xticklabels(), visible = False)

            # Settings for collage
            # don't show subplots
            ax_list[17].axis('off')
            ax_list[18].axis('off')
            ax_list[19].axis('off')

            # Show legend
            ax_list[11].legend(bbox_to_anchor=(2.0, -1.15, 2.0, 0.102),
                               loc = 3, ncol = 4, mode = "expand", borderaxespad = 0.0)
            # Plot title
            plt.title('OCN plunt functional types (PFT, %) at stations',
                      size = fsize + 4, x = -2.0, y = 4.8)

            # Subplots positions, save plot and clean memory:
            plt.tight_layout(pad = 10.0, w_pad = 0.5, h_pad = 5)
            plt.savefig(
                data_OUT + f'PFT_in_{lst4lc_ds[j]}.png',
                format = 'png',
                dpi = 300,
            )
            plt.close(fig)
            plt.gcf().clear()

    # -- Select and find difference between refer and OCN simulations:
    #    a. Get reference dataset and remove it from lst4ba_ds
    for i in range(len(lst4ba_ds)):
        if lst4ba_ds[i] == refer:
            ref = lst4ba.pop(i)
    #    b. Get difference between experiments (refer - similation)
    diff_ba = [ref[param_BA] - lst4ba[i][param_BA] for i in range(len(lst4ba))]

    # -- Create histogram for each PFT:
    if lba_hist:
        print('Working on Burned area bar chart and data \n')
        # -- Cycle by datasets:
        for i in range(len(lst4lc_ds)):
            data4pft = []
            # -- Cycle by PFT:
            for j in range(len(pft4simulations[i])):
                # -- Define burned area in each PFT:
                ba4pft = pd.Series(
                    (diff_ba[i] * pft4simulations[i][j]).sum(dim = {'lat', 'lon'}).data)
                # -- Create a timeseries with PFT names:
                zeros = pd.Series(
                    pft_sname[j], index = np.arange(0, len(pft4simulations[i][j].data), 1))
                # -- Add these data in dataframe and add dataframe to a new list
                data4pft.append(pd.concat([ba4pft, zeros], axis = 1))
            # -- Accumulation of all PFTs data into one dataframe:
            df4allpft = pd.concat(data4pft, axis = 0)
            df4allpft = (df4allpft.rename(columns = {0 : 'data', 1 : 'PFT'})
                                  .reset_index(drop = True))
            # -- Save data:
            df4allpft.to_csv(
                data_OUT + f'Data4PFT_{lst4lc_ds[i]}_{refer}.csv',
                float_format = '%.2f',
                sep = ';',
                index = True,
            )

            # -- Visualisation of the results:
            # Settings for bar plots
            hx_label  = 'Difference 1000 km\u00B2'
            hy_label  = 'Count'
            plt_title = (f'Burned area difference ({refer} - {lst4lc_ds[i]}) for \n'
                         f'different PFTs from {t_start} to {t_stop} over {region} region')
            pout      = data_OUT + f'BA_DIFF_{lst4lc_ds[i]}_{refer}.png'

            if lst4lc_ds[i] in ('OCN_S2Prog', 'OCN_S2Prog_v3', 'OCN_S2Prog_v4'):
                ymin_ba = -3500.0
                ymax_ba =  500.0
            else:
                ymin_ba = -50.0 #-100.0
                ymax_ba =  50.0 # 250.0
            # Create plots:
            plot_diff_hist(
                df4allpft,
                lst4lc_ds[i],
                plt_title,
                hx_label,
                hy_label,
                ymin_ba,
                ymax_ba,
                pout,
            )
    print('END program')
    # =============================    End of program   ====================
