# -*- coding: utf-8 -*-
"""
Script for analysis and visualization data, presented as a point (station)

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de


History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-07-21 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-14 Evgenii Churiulin, MPI-BGC
           Adapted  for the new format of input functions, changed the format 
           of path to the personal modules
    1.3    2023-05-04 Evgenii Churiulin, MPI-BGC
           Small changes in code related to refactoring
"""

# =============================     Import modules     ====================
# -- Standard modules:
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
# -- Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.user_settings import stations, plt_limits_point
from calc.vis_controls import one_linear_plot, box_plot
from libraries.lib4sys_support import makefolder
from libraries.lib4visualization import vis_stations

# =============================   Personal functions   ====================

# Function: one_point_calc. Create option for analysis data in one point
#                           (station) or in a random point
def one_point_calc(
        # Input variables:
        lst4ds_names:list[str],        # Dataset names
        data_list:list[xr.DataArray],  # Data for research datasets
        var:str,                       # Research parameter
        lvar_name:str,                 # Long name of the research parameter
        svar_name:str,                 # Short name of the research parameter
        data_OUT:str,                  # Output path
        region:str,                    # Research region
        # OUTPUT variables:
    ) -> pd.DataFrame:                 # Statistical data for all stations
    # -- Local variables:
    # Select parameters with simular units:
    units_group_1 = ('burned_area')                       # km2
    units_group_2 = ('npp', 'gpp', 'nee', 'nbp', 'fFire') # gC m-2 yr-1
    units_group_3 = ('cVeg', 'lai')                       # kg C m-2 and m2 m-2

    fn_output = 'STATIONS'     # Name of output folder
    csv_output = 'Stat4points' # Name of output for table with statistical data

    g2kg = 1000 # gramm in 1 kg

    # -- Create output folder:
    data_OUT = makefolder(data_OUT + fn_output)

    # -- Get data for stations and create figures:
    for i in range(len(stations)):
        # -- Get coordinates for each point:
        lats      = stations.get(i + 1)[0]
        lons      = stations.get(i + 1)[1]
        name4plot = stations.get(i + 1)[2]
        pft4plot  = stations.get(i + 1)[3]
        # -- Get data for each station:
        lst4points = []
        for j in range(len(lst4ds_names)):
            point_data = data_list[j][var].sel(lat = lats, lon = lons, method = 'nearest')
            # 2.2.1 Convert parameters to correct units:
            if var in units_group_1:
                var_units = '1000 km2'
                lst4points.append(point_data)
            elif var in units_group_2:
                # Convert units from gC m-2 yr-1 --> kgC m-2 yr-1
                var_units = 'kg C m\u207b\u00B2 yr\u207b\u00B9'
                lst4points.append(point_data / g2kg )
            elif var in units_group_3:
                var_units = 'kg C m \u207b\u00B2' if var == 'cVeg' else 'm\u00B2 m\u207b\u00B2'
                lst4points.append(point_data)

        # -- Get data for statistical metrics and save them into .csv tables:
        stat_data = []
        for j in range(len(lst4ds_names)):
            stat_data.append(pd.Series(lst4points[j].data, name = lst4ds_names[j]))
        df_stat_data = pd.concat(stat_data, axis = 1)
        # Get standard statistical parameters based on describe method:
        general_stat = df_stat_data.describe()
        stat_OUT = f'{csv_output}_{var}.csv'
        # Delete old file:
        if (os.path.exists(data_OUT + stat_OUT) and i == 0):
            os.remove(data_OUT + stat_OUT)
        # Create a new file:
        general_stat.to_csv(
            data_OUT + stat_OUT,
            float_format = '%.3f',
            sep = ';',
            index = True,
            mode = 'a',
        )

        # -- Get data for boxplots:
        boxplot_data = []
        for j in range(len(lst4ds_names)):
            boxplot_data.append(
                pd.concat(
                    [pd.Series(lst4ds_names[j], index = np.arange(0, len(lst4points[j].data), 1)),
                     pd.Series(lst4points[j].data)], axis = 1
                )
            )
        df_boxplot_data = (
            pd.concat(boxplot_data, axis = 0)
              .rename(columns = {0 : 'dataset',  1 : 'data'})
        )

        # -- User settings for boxplots and line plots:
        user_plt_settings = {
            'title'           : (f'Annual values of {lvar_name} for one point '
                                 f'(lat = {point_data[0].lat.values},'
                                 f' lon = {point_data[0].lon.values}) \n {pft4plot}'),
            'ylabel'          : f'{svar_name}, {var_units}',
            'output_name'     : f'{var}_station_{name4plot}.png',
            'output_name_bxp' : f'boxplot_{var}_station_{name4plot}.png',
            'legend_pos'      : 'upper left',
        }
        # Define limits for y axis (min, max, step)
        ymin  = plt_limits_point.get(var)[0]
        ymax  = plt_limits_point.get(var)[1]
        ystep = plt_limits_point.get(var)[2]
        # Apply additional settings for uniq plots:
        if (var == 'cVeg' and (i in [0, 9])):
            ymin  = 10.0
            ymax  = 30.1
            ystep =  5.0
        elif (var == 'cVeg' and (i in [1, 6])):
            ymin  = 0.0
            ymax  = 6.1
            ystep = 0.5
        elif (var == 'cVeg' and (i in [2, 11, 12, 14, 15])):
            ymin  = 0.0
            ymax  = 3.1
            ystep = 0.25
        elif (var == 'cVeg' and (i in [4, 16])):
            ymin  =  0.0
            ymax  = 10.1
            ystep =  1.0
        elif (var == 'lai' and (i == 0 or i == 9)):
            ymin  =  6.0
            ymax  =  9.1
            ystep =  1.0
        elif (var == 'burned_area' and (i in [0, 3, 4, 5, 6, 7, 9, 14])):
            ymin  =  0.0
            ymax  =  0.51
            ystep =  0.05
        elif (var == 'fFire' and (i in [0, 3, 5, 7, 9])):
            ymin  =  0.0
            ymax  =  0.051
            ystep =  0.01
        # -- Start visualization:
        # Plot 1: linear plot for each station
        one_linear_plot(
            lst4ds_names,
            region,
            var,
            lst4points,
            user_plt_settings,
            data_OUT,
            point_mode = True,
            ymin = ymin,
            ymax = ymax,
            ystep = ystep,
        )
        # Plot 2: Boxplot for each station
        box_plot(
            df_boxplot_data,
            user_plt_settings,
            data_OUT,
            ymin,
            ymax,
            ystep,
        )
        # Plot 3: 2D Map with station location
        vis_stations(data_OUT)

    return df_stat_data
