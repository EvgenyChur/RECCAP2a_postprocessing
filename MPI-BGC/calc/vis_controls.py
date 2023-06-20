# -*- coding: utf-8 -*-
"""
The module has functions which are related to the visualization module.

The main purpose of the functions which are presented in this module is control
of visualization operations from vis_module.

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  561 804-6142
email:  evchur@bgc-jena.mpg.de  


History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-07-05 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
    1.2    2022-11-11 Evgenii Churiulin, MPI-BGC
           Add new functions, adapted  for the new format of input functions,
           changed the format of path to the personal modules
    1.3    2023-05-04 Evgenii Churiulin, MPI-BGC
           Code refactoring
    1.4    2023-05-15 Evgenii Churiulin, MPI-BGC
           a. Transfered and adapted get_figure4lcc function from scripts ba_esa_pft.py
           and ba_ocn_pft.py
           b. Transfered and adapted pft_plot function from check_ocn_pft.py
"""

# =============================     Import modules     ====================
# 1.1: Standard modules
import os
import sys
import numpy as np
import xarray as xr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Optional

# 1.2 Personal module
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.user_settings import (
    time_limits, plt_limits, clb_limits, layout_settings, clb_diff_limits)
from libraries import lib4visualization as vis
from libraries import lib4colors as lcolor

# =============================   Personal functions   ====================

# 2.1 Function --> line_settings. Define relevant color and style for lines
#                  depending on name of your research simulation
def line_settings(
        # Input variables:
        lst4dsnames:list[str],              # Research datasets
        # OUTPUT variables:
    ) -> tuple[
                list[dict],                 # Line colors for research simulations;
                list[dict],                 # Line styles for your research simulations.
    ]:
    # Local variables:
    tcolor = 0 # index of colors in dict 
    tstyle = 1 # index of styles in dict 

    clr = []
    stl = []
    for name in lst4dsnames:
        clr.append(lcolor.xfire_colors.get(name)[tcolor])
        stl.append(lcolor.xfire_colors.get(name)[tstyle])
    return clr, stl

# 2.2 Function --> one_linear_plot (1D). Create linear plot based on the research parameters
def one_linear_plot(
        # Input variables:
        dtset_list:list[str],               # Datasets names
        region:str,                         # Research domain
        param_var:str,                      # Research parameter
        data:list[xr.DataArray],            # List with datasets data
        user_plt_settings:dict,             # User settings for plots (you can set them in fire_xarray.py)
        data_OUT:str,                       # Output path for the figure
        point_mode: Optional[bool] = False, # Do you want to use this function in one_point.py script?
        ymin: Optional[float] = None,       # Limits for y axis (min)
        ymax: Optional[float] = None,       # Limits for y axis (max)
        ystep: Optional[float] = None,      # Limits for y axis (step)
        # OUTPUT variables:
    ):                                      # Create new figure in output folder

    # 1. Define settings for plots (title, labels, legend position and plot name)
    plt_title   = user_plt_settings.get('title')
    ylabel      = user_plt_settings.get('ylabel')
    leg_loc     = user_plt_settings.get('legend_pos' )
    output_name = user_plt_settings.get('output_name')

    # 2. Define format settings for x and y axes depending on the actual mode 
    #    and research parameter:
    if point_mode == False:
        version = 'netcdf_lplot'
        # Set limits for y axis (min, max, step)
        ymin    = plt_limits.get(region).get(param_var)[0]
        ymax    = plt_limits.get(region).get(param_var)[1]
        ystep   = plt_limits.get(region).get(param_var)[2]
    else:
        version = 'lplots_stomata2'
    # 3. Define limits for x axis
    frs_yr = time_limits.get(param_var).get('OCN')[0]
    lst_yr = time_limits.get(param_var).get('OCN')[1]
    # Apply corrections for x axis (time step, first year, last year )
    tstep  = 2 if (lst_yr - frs_yr) <= 26 else 5
    frs_yr = frs_yr - (frs_yr % tstep)          if frs_yr % tstep != 0 else frs_yr
    lst_yr = lst_yr + (tstep  - lst_yr % tstep) if lst_yr % tstep != 0 else lst_yr

    # -- Get settings for line colors and styles:
    colors, styles = line_settings(dtset_list)
    # -- Create linear plot based on NetCDF data:
    line_plot = vis.netcdf_line_plots(
        len(dtset_list),
        data,
        dtset_list,
        colors,
        styles,
        point_mode,
    )
    # -- Apply settings for linear plots:
    vis.line_plot_settings(
        line_plot,
        version,
        plt_title,
        ylabel,
        leg_loc,
        ymin,
        ymax,
        ystep,
        frs_yr,
        lst_yr + 1,
        tstep,
    )
    # Save plot and clean memory:
    plt.savefig(data_OUT + output_name, format = 'png', dpi = 300)
    plt.gcf().clear()

# 2.3 Function ---> box_plot (1D). Create boxplot for stations
def box_plot(
        # Input variables:
        df:pd.DataFrame,                           # Research data
        user_plt_settings:dict,                    # User settings for plots (you can set them in one_point.py)
        data_OUT:str,                              # Output path
        ymin:float,                                # Limits for y axis (min)
        ymax:float,                                # Limits for y axis (max)
        ystep:float                                # Limits for y axis (step)
        # OUTPUT variables:
    ):                                             # Create new figure in output folder
    # 1. Define settings for plots (title, labels, legend position and plot name)
    plt_title   = user_plt_settings.get('title')
    ylabel      = user_plt_settings.get('ylabel')
    xlabel      = 'Available datasets'
    output_name = user_plt_settings.get('output_name_bxp')
    clr         = 'black' # color
    fsize       = 14      # text size
    lpab        = 20      # label pad

    # 2. Create area for plot
    fig = plt.figure(figsize = (12,7))
    ax  = fig.add_subplot(111)
    ax  = sns.boxplot(x = 'dataset', y = 'data', data = df)

    # 3. Settings for plots
    ax.set_title(plt_title, color = clr, fontsize = fsize, pad      = lpab)
    ax.set_xlabel(xlabel  , color = clr, fontsize = fsize, labelpad = lpab)
    ax.set_ylabel(ylabel  , color = clr, fontsize = fsize, labelpad = lpab)
    # y axis limits
    ax.set_yticks(np.arange(ymin, ymax, ystep))
    # parameters for ticks: rotation, size
    vis.tick_rotation_size(ax, 15, fsize)
    # 4. Grid settings
    ax.grid(True , which     = 'major' ,
                   color     = 'grey'  ,   # black
                   linestyle = 'dashed',   # solid
                   alpha     = 0.2     )   # 0.5
    # Save plot and clean memory
    plt.savefig(data_OUT + output_name, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()

# 2.4 Function ---> one_plot (2D). Create plot for mean, std or trend.
def one_plot(
        # Input variables:
        dtset_list:list[str],                      # Names of the actual datasets
        p_mode:str,                                # Type of data (mean, std, trends)
        region:str,                                # Research domain (Global, Europe, Tropics, NH, Other)
        lon:list[np.array],                        # 1D arrays with longitudes
        lat:list[np.array],                        # 1D arrays with latitudes
        data:list[xr.DataArray],                   # 2D data for visualization (mean, std, trends)
        var:str,                                   # Reseach parameter (fire, biomass, npp, gpp, lai, cVeg)
        ylabel:list[str],                          # Y axis labels
        title:list[str],                           # Plot titles
        path_OUT:list[str],                        # Plot output paths
        # OUTPUT variables:
    ):                                             # Create new figure in output folder
    # Define limits and colormap scheme for colorbars
    clb_lim = clb_limits.get(region)
    # Create figure
    for i in range(len(dtset_list)):
        print(f'Plot {p_mode} for {dtset_list[i]} over {region} region')
        fig  = plt.figure(figsize = (8,8))
        ax   = fig.add_subplot(111)
        plot = vis.netcdf_grid(
            ax, region  , lon[i], lat[i], data[i], p_mode, var, clb_lim, ylabel,
                title[i], ltitle = True,
        )
        # Save plot and clean memory
        plt.savefig(path_OUT[i], format = 'png', dpi = 300)
        plt.close(fig)
        plt.gcf().clear()

# 2.5 Function ---> collage_plot (2D). Create collage plot for mean, std or trend.
def collage_plot(
        # Input variables:
        dtset_list:list[str],                  # Names of the research datasets
        region:str,                            # Research domain
        lon:list[np.array],                    # 1D arrays with longitudes
        lat:list[np.array],                    # 1D arrays with latitudes
        lst4mean:list[xr.DataArray],           # 2D arrays with mean values
        lst4std:list[xr.DataArray],            # 2D arrays with STD values
        lst4trends:list[xr.DataArray],         # 2D arrays with time trend values
        var:str,                               # Reseach parameter
        bm_ylabel:list[str],                   # label of y axis
        c_title:str,                           # plot title
        c_path_OUT:str,                        # output path
        ldiff: Optional[bool] = False,         # Do you want to create difference plot?
        refer: Optional[str] = None,           # Name of the reference dataset
        comp_ds: Optional[str] = None,         # Name of the research dataset
        clb_uniq: Optional[list[dict]] = None, # Use uniq user settings from fire_ratio.py
        # OUTPUT variables:
    ):                                         # Create new figure in output folder
    # Local variables:
    nrows_num = 3 # row numbers for collage plot

    # Define limits and colormap scheme
    if var == 'ratio':
        clb_lim = clb_uniq
    else:
        clb_lim = clb_limits.get(region)

    # -- Settings for position of subplots on the figure:
    # Get actual values
    pad   = layout_settings.get(region).get(len(dtset_list))[0]
    w_pad = layout_settings.get(region).get(len(dtset_list))[1]
    h_pad = layout_settings.get(region).get(len(dtset_list))[2] 
    lens  = layout_settings.get(region).get(len(dtset_list))[3] 
    higt  = layout_settings.get(region).get(len(dtset_list))[4] 

    # -- Start visualization:
    fig, axes = plt.subplots(
        nrows = nrows_num,
        ncols = len(dtset_list),
        figsize = (lens, higt),
    )
    # -- Define data for visualization:
    for i, dtset_name in enumerate((dtset_list)):
        if ldiff == True:
            if i == (len(dtset_list) - 1):
                lims = clb_diff_limits.get(region)
            else:
                lims = clb_lim
            m_data = lst4mean[i].values
            s_data = lst4std[i].values
            t_data = lst4trends[i].values
        else:
            lims   = clb_lim
            m_data = lst4mean[i]
            s_data = lst4std[i]
            t_data = lst4trends[i]
        # -- Create plots (MEAN, STD, Trends)
        bm_map = vis.netcdf_grid(axes[0, i] , region, lon[i], lat[i], m_data,
                                 'mean', var, lims  , bm_ylabel)
        bm_map = vis.netcdf_grid(axes[1, i] , region, lon[i], lat[i], s_data,
                                 'std' , var, lims  , bm_ylabel)
        bm_map = vis.netcdf_grid(axes[2, i] , region, lon[i], lat[i], t_data,
                                'trend', var, lims  , bm_ylabel)
        # -- Add labels
        axes[0, 0].set_ylabel('MEAN')
        axes[1, 0].set_ylabel('STD')
        axes[2, 0].set_ylabel('TREND')

    for ax in axes.flat:
        ax.axes.get_xaxis().set_ticklabels([])
        ax.axes.get_yaxis().set_ticklabels([])
        ax.axes.axis("tight")
        ax.set_xlabel("")

    for i, dtset_name in enumerate((dtset_list)):
        if ldiff == True:
            axes[0, 0].set_title(refer       )
            axes[0, 1].set_title(comp_ds     )
            axes[0, 2].set_title(f'Difference \n({refer} - {comp_ds})')
        else:
            axes[0, i].set_title(dtset_name)
    # Set subplot positions and add plot title
    plt.tight_layout(pad = pad, w_pad = w_pad, h_pad = h_pad) 
    fig.suptitle(c_title, fontsize = 16) #y=1.02
    # Save plot and clean memory
    plt.savefig(c_path_OUT, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()

# 2.6 get_figure4lcc --> Create collage figure with information about burned area
#                        for different data sources:
#                        a. vegetation classes based on ESA-CCI MODIS 5.1 dataset (ba_esa_pft.py)
#                        b. vegetation classes based on OCN datasets (ba_ocn_pft.py)
def get_figure4lcc(
        # Input variables:
        rows:int,                      # Row numbers (for subplot)
        cols:int,                      # Column numbers (for subplot)
        lon:'np.ndarray[float]',       # Longitude
        lat:'np.ndarray[float]',       # Latitude
        lst4data:list[xr.DataArray],   # Research datasets
        mf4analysis:str,               # Research parameter (burned_area, fFire, cVeg, npp, gpp, lai)
        param:str,                     # Statistical parameter (mean, std, trend)
        clb_lim:list[dict],            # Subplot settings (colorbar, ranges and ets)
        region:str,                    # Research domain (Global, Europe, Tropics, NH, Other).
        title:list[str],               # Plot subtitles for each ESA-CCI PFT
        plt_name:str,                  # Plot title
        path_exit:str,                 # Output path
        # OUTPUT variables:
    ):                                 # Create collage plot
    # -- Local variables:
    ylabel = '1000 km\u00B2'
    # -- Add auto correction of actual subplots position:
    #                   pad, w_pad, h_pad  fonsize
    rset = {'Global' : [5.0,  0.05,  6.5,     16],
            'Europe' : [4.0,  0.05,  0.0,     16]}
    # -- Visualization part:
    fig = plt.figure(figsize = (14,10))
    # Create grid
    egrid = (rows, cols)
    ax_list = []
    for i in range(egrid[0]):
        for j in range(egrid[1]):
            ax_list.append(plt.subplot2grid(egrid, (i, j), rowspan = 1, colspan = 1))
    # -- Add data to subplots:
    for i in range(len(lst4data)):
        plot = vis.netcdf_grid(
            ax_list[i],
            region,
            lon,
            lat,
            lst4data[i],
            param,
            mf4analysis,
            clb_lim,
            ylabel,
            title[i],
            ltitle = True,
        )
    # -- Apply settings for subplot locations:
    plt.tight_layout(
        pad = rset.get(region)[0],
        w_pad = rset.get(region)[1],
        h_pad = rset.get(region)[2],
    )
    # -- Add subplot titles:
    fig.suptitle(plt_name, fontsize = rset.get(region)[3])
    # -- Save plot and clean memory
    plt.savefig(path_exit, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()

# 2.7 pft_plot --> Create linear plots for different PFT:
def pft_plot(
        # Input variables:
        data:list[xr.DataArray],          # Research datasets
        settings:dict,                    # Plot settings (legend, colors, styles, limits)
        ptype:str,                        # PFT group
        pout:str,                         # Output path for figure
        # Output variables:
    ):                                    # Create a new plot in output folder
    # -- Plot settings:
    mode_set  = 'lplots_stomata2'
    plt_title = 'Comparison of PFT groups based on OCN and ESA-CCI MODIS data'
    ylabel    = 'Burned area, 1000 km\u00B2'
    leg_loc   = 'upper right'
    legends   = settings.get(ptype).get('legend')
    colors    = settings.get(ptype).get('color')
    styles    = settings.get(ptype).get('style')
    ylim      = settings.get(ptype).get('ylim')
    # -- Plot processing:
    fig = plt.figure(figsize = (12,7))
    ax  = fig.add_subplot(111)
    # Create plot:
    line_plot = vis.netcdf_line_plots(
        len(data),
        data,
        legends,
        colors,
        styles,
        point_mode = True,
    )
    # Settings for plots:
    vis.line_plot_settings(
        line_plot,
        mode_set,
        plt_title,
        ylabel,
        leg_loc,
        ylim[0],
        ylim[1],
        ylim[2],
    )
    # -- Save plot and clean memory:
    plt.savefig(pout + f'PFT_{ptype}.png', format = 'png', dpi = 300)
    plt.gcf().clear()
# =======================================================================
