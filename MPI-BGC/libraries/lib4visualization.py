# -*- coding: utf-8 -*-

"""
Module with functions for visualization:

The program contains functions:
    # Section for plots line plots
    1. line_plots         ---> Visualization of plots based on timeseries
    2. netcdf_line_plots  ---> Visualization of plots based on NetCDF
    3. plots5_stomata     ---> Visualization stomatal resistance data
    4. vis_stat_mode      ---> Visualization of data from stat_module 
                               (annual cycle - full             --> was get_m ;
                                annual cycle - 2 - 4 parameters --> was get_2m;
                                daily  cycle - full             --> was get_d ;
                                diurnal cycle - full            --> was get_u ;
                                user time interval (e.q: 1 week)--> was get_h )

    # Section for line plots settings
    1. tick_rotation_size ---> settings for numbers on the axis of plot 
    2. line_plot_settings ---> settings for AxesSubplot 

    # Section for Taylor diagram
    1. Taylor diagram     ---> plot Taylor diagram  

    # Section for NetCDF grid visualizatuion (new)
    1 select_domain       ---> domain settings for netcdf_grid and grid_series functions
    2. vis_stations       ---> create global map with stations location;
    3. netcdf_grid        ---> create map for selected research domain and parameter
                               based on corresponding datasets with statistical data
                               (MEAN, STD, TIME TREND);
    4. netcdf_grid_series ---> create maps for selected research domain and parameters
    5. create_fast_xarray_plot --> create simple domain map based on xarray options
                                   for visualization;

    # Have to be corrected and modernized
    1. get_data_m
    2. plot_waves         ---> heat and cold waves visualization

Autors of project from 2020.08.01 - 2022.05.31:
Evgenii Churiulin, Merja Tölle, Center for Enviromental System Research (CESR) 

Autors of project from 2022.06.01 - current:
Evgenii Churiulin, Ana Bastos, Max Planck Institute for Biogeochemistry (MPI-BGC)

Acknowledgements: Vladimir Kopeikin, Denis Blinov, Yannick Copin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  561 804-6142
email:  evchur@bgc-jena.mpg.de  

History:
Version    Date       Name
---------- ---------- ----
    1.1    2021-06-18 Evgenii Churiulin, Center for Enviromental System Research (CESR)
           Initial release
    1.2    2022-06-22 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Change several functions for line plots and 2 functions for grid
           data visualization was added. New functions have names:
           line_plots, netcdf_line_plots, netcdf_lplot_set, netcdf_grid, 
           netcdf_grid_series
    1.3    2022-06-24 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Correted functions for plot settings. All of them are included in one
    1.4    2022-08-18 Evgenii Churiulin, MPI-BGC. Added new function for
           visualization of burned area difference for different PFT 
    1.5    2022-10-10 Evgenii Churiulin, MPI-BGC. Updated next functions:
           1 - netcdf_grid, 2 - netcdf_grid_series -- created new option for domain
           settings, get_m, get_2m, get_d --> converted to one function vis_stat_mode
           new functions for domain settings and parameters settings were created
    1.6    2023.05.05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================== Import modules ===================
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
from typing import Optional
# Import special methods for ticks and ocean mask
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.basemap import Basemap, maskoceans
# Switch off python warnings
import warnings
warnings.filterwarnings("ignore")
# Import personal module
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings import user_settings as uset

# =============================   User settings   ========================
# -- Additional parameters for X and Y axis for plots
minorLocator   = AutoMinorLocator (n=5)
minorFormatter = FormatStrFormatter('%.1f')

years = mdates.YearLocator() #every year
days = mdates.DayLocator(15)
yearFmt = mdates.DateFormatter('%Y')

# =============================   Personal functions   ===================

# Section 1: Simple plots:
# ========================================================================
# 1. line_plots --> Create plot (line, scatter, bar) based on data presented as timeseries.
def line_plots(
        # Input variables:
        ax:plt.Axes,                           # Axis-object of matplotlib-subplots
        lines_count:int,                       # Number of lines for visualization
        data:list[pd.Series],                  # Timeseries for visualization. Each timeseries has to be in
                                               # next format: Timeindex - Parameter
        legends:list[str],                     # Line labels
        colors:list[str],                      # Line colors
        styles:list[str],                      # Line styles
        plt_type: Optional[str] = 'line_plot', # Type of the plots
        # OUTPUT variables:
    ):                                         # Create new figure in output folder
    # Start visualization:
    # -- Line plots:
    if plt_type == 'line_plot':
        for i in range(lines_count):
            ax.plot(data[i].index, data[i],
                    label = legends[i],
                    color =  colors[i],
                    linestyle = styles[i])

    # -- Scatter plots:
    if plt_type == 'scatter':
        for i in range(lines_count):
            ax.scatter(data[i].index, data[i],
                       # Settings for legend, line color and line style
                       label     = legends[i], 
                       color     =  colors[i],
                       linestyle =  styles[i])

    # -- Bar plots:
    if plt_type == 'bar':
        for i in range(lines_count):
            ax.bar(data[i].index, data[i],
                   # Settings for legend, line color and line style
                   label     = legends[i],
                   color     =  colors[i],
                   linestyle =  styles[i])
# ----------------------------------------------------------------------

# 2. netcdf_line_plots --> Visualization of the data from NetCDF files after xarray
#                          post-processing. In this function you can choose the
#                          actual number of lines for visualization.
#
#                          Data should be in one point (or for all grid accumulated
#                          to one point)
def netcdf_line_plots(
        # Input variables:
        lines_count:int,                       # Number of lines for visualization
        data:list[xr.DataArray],               # Data for visualization
        legends:list[str],                     # Line labels
        colors:list[str],                      # Line colors
        styles:list[str],                      # Line styles
        point_mode:bool,
        # OUTPUT variables:
    ):                                         # Create new figure in output folder
    # -- Create figure:
    fig = plt.figure(figsize = (12,7))
    ax = fig.add_subplot(111)
    # -- Add data to figure:
    for i in range(lines_count):
        if point_mode == True:
            index = data[i].time
        else:
            index = data[i].year

        ax.plot(
            index,
            data[i].values,
            label = legends[i],
            color = colors[i],
            linestyle = styles[i],
        )
    return ax
# ----------------------------------------------------------------------

# 3. plots5_stomata --> Create stomatal resistance plot
def plots5_stomata(
        # Input variables:
        ax:plt.Axes,                           # Axis-object of matplotlib-subplots
        lst4ts:list[pd.Series],                # Timeseries with stomatal resistance data
        lst4leg:list[str],                     # Line labels
        # OUTPUT variables:
    ):
    # Start visualization
    # Line colors:
    clr = ['blue', 'green', 'brown', 'red', 'black']
    # Line styles:
    lst = ['-'   , '-'    , '-'    , '-'  , 'o'    ]

    for i in range(len(lst4ts)):
        # The last element of data list has information about data errors:
        if i == len(lst) - 1:
            ax.errorbar(
                lst4ts[i].index,
                lst4ts[i],
                label = leg[i],
                color = clr[i],
                fmt = lst[i],
                yerr = 10,
                ecolor = 'gray',
                #linewidths = 3.5
            )
        else:
            ax.plot(
                lst4ts[i].index,
                lst4ts[i],
                label = leg[i],
                color = clr[i],
                linestyle = lst[i],
            )
# ----------------------------------------------------------------------

def create_lplot_with_2axis(
        # Input variables:
        lst4data:list[pd.DataFrame],    # Research data
        plt_settings:dict,              # User settings for plot
        # Output variables
    ):                                  # Create figure in output folder
    # -- Local variables:
    legends = plt_settings.get('labels')
    colors  = plt_settings.get('colors')
    styles  = plt_settings.get('styles')
    cols    = plt_settings.get('columns')
    # Settings for plot title and labels:
    title   = plt_settings.get('title')
    ylabel1 = plt_settings.get('ylabel_ax1')
    ylabel2 = plt_settings.get('ylabel_ax2')
    # Settings for text colors, pads, rotation and size:
    clr     = plt_settings.get('clr')
    fsize   = plt_settings.get('fsize')
    pads    = plt_settings.get('pad')
    rotat   = plt_settings.get('rotation')
    # Settings for legends:
    loc1    = plt_settings.get('loc_ax1')
    loc2    = plt_settings.get('loc_ax2')
    frame   = plt_settings.get('leg_frameon')
    # Settings for output files:
    pout    = plt_settings.get('output')
    fout    = 'png'
    dpi     = 300
    # Recalculation coefficients:
    ret_coef = 1e9 # m2 in 1000 km2
    # -- Start visualization:
    fig = plt.figure(figsize = (12,7))
    ax = fig.add_subplot(111)
    # twin object for two different y-axis on the sample plot
    ax2 = ax.twinx()
    # -- Add line objects:
    for i in range(len(lst4data)):
        if i in (0, 2):
            ax.plot(
                lst4data[i].index,
                lst4data[i][cols[i]] * ret_coef,
                label = legends[i],
                color = colors[i],
                linestyle = styles[i],
            )
        else:
            ax2.plot(
                lst4data[i].index,
                lst4data[i][cols[i]],
                label = legends[i],
                color = colors[i],
                linestyle = styles[i],
            )
    #  -- Settings for labels and titles:
    ax.set_title(    title, color = clr, fontsize = fsize, pad      = pads)
    ax.set_ylabel( ylabel1, color = clr, fontsize = fsize, labelpad = pads)
    ax2.set_ylabel(ylabel2, color = clr, fontsize = fsize, labelpad = pads)
    # -- Settings for axis:
    tick_rotation_size(ax , rotat, fsize)
    tick_rotation_size(ax2, rotat, fsize)
    # -- Settings for legend:
    ax.legend( loc = loc1, frameon = frame)
    ax2.legend(loc = loc2, frameon = frame)
    # -- Save plot and clean memory:
    plt.savefig(pout, format = fout, dpi = dpi)
    plt.close(fig)
    plt.gcf().clear()


# Section 2: Line plot settings
# ======================================================================

# 1. tick_rotation_size --> Additional setting for x and y axis
def tick_rotation_size(
                        # Input variables:
                        ax:plt.Axes,                               # Axis-object of matplotlib-subplots
                        rotation:int,                              # Rotation of numbers in y and x axis
                        fsize:int,                                 # Size of numbers in y and x axis
                        # OUTPUT variables:
                      ):                                           # Figure with corrected ticks
    # -- Set size and position of x and y values (ticks):
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(rotation)
        label.set_fontsize(fsize)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(fsize)

# 2. line_plot_settings --> Special function with additional settings for line plots
def line_plot_settings(
        # Input variables:
        ax:plt.Axes,                           # Axis-object of matplotlib-subplots
        version:str,                           # Actual script, which you use for running this function
        plt_label:str,                         # Plot title
        y_label:str,                           # Plot label for y axis
        leg_pos:str,                           # Legend location
        y_min:float,                           # Limits for y axis (min)
        y_max:float,                           # Limits for y axis (max)
        y_step:float,                          # Limits for y axis (step)
        yr_start: Optional[int] = None,        # First year. Default is None
        yr_stop: Optional[int] = None,         # Last year. Default is None
        yr_step: Optional[int] = None,         # Timestep. Default is None
        lx_label: Optional[bool] = False,      # Turn on x label. Default is False
        x_label: Optional[str] = None,         # Actual x axis label. Default is None
        p_start: Optional[str] = None,         # First time moment ('2010-01-01'). Default is None
        p_stop: Optional[str] = None,          # Last time moment ('2020-01-01'). Default is None
        llegend: Optional[bool] = True,        # Add plot legend. Default is True
        lsecond_axis: Optional[bool] = False,  # Add second axis. Default is False
        # OUTPUT variables:
    ):                                         # Figure with user settings
    # -- Get actual fontsize, pad (labelpad) and rotation of ticks:
    #                                fsize   lpab   rotation    color
    settings = {'dplot'          : [   14,    20,     0,        'black' ],
                'lplots_stomata' : [   18,    20,    15,        'black' ],
                'lplots_stomata2': [   16,    20,     0,        'black' ],
                'modis_plots'    : [   14,    20,    15,        'black' ],
                'lplot'          : [   14,    20,    15,        'black' ],
                'netcdf_lplot'   : [   14,    20,     0,        'black' ]}
    
    fsize    = settings.get(version)[0]
    lpab     = settings.get(version)[1]
    rotation = settings.get(version)[2]
    clr      = settings.get(version)[3]

    # -- Set plot title
    ax.set_title(plt_label, color = clr, fontsize = fsize, pad = lpab)
    
    # -- Set labels for axis:
    if lx_label == True:
        ax.set_xlabel(x_label, color = clr, fontsize = fsize, labelpad = lpab)
    ax.set_ylabel(    y_label, color = clr, fontsize = fsize, labelpad = lpab)

    # -- Legend parameters
    font = font_manager.FontProperties(family = 'Arial', style = 'normal', size = fsize)

    if llegend == True:
        #ax.legend(loc = leg_pos, frameon = True, prop = font, bbox_to_anchor=(0.5, -0.05),)
        ax.legend(loc=leg_pos,  ncol=1,prop = font, frameon = True,)

    # -- Get x ticks parameters (you can use different options):
    if version == 'dplot':
        ax.set_xlim(p_start, p_stop)
        xftm = mdates.DateFormatter('%H')
        ax.xaxis.set_major_formatter(xftm)

    elif version == 'lplot':
        ax.set_xlim(p_start, p_stop)
        xftm = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(xftm)
        ax.xaxis.set_minor_locator(days)

    elif version in ('lplots_stomata', 'modis_plots'):
        xftm = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(xftm)
        ax.xaxis.set_minor_locator(days)

    elif version == 'lplots_stomata2':
        xftm = mdates.DateFormatter('%Y') #'%B') #'%d-%m')   #%m-%d  '%B'
        ax.xaxis.set_major_formatter(xftm)
        ax.xaxis.set_minor_locator(years)

    elif version == 'netcdf_lplot':
        ax.set_xticks(np.arange(yr_start, yr_stop, yr_step))

    # -- Get y ticks parameters:
    ax.set_yticks(np.arange(y_min, y_max, y_step))

    if lsecond_axis == True:
        ax.tick_params(axis = 'y' , which ='major', bottom = True  , top = False,
                       left = True, right = True  , labelleft ='on', labelright = 'on')
        ax.tick_params(axis = 'y' , which ='minor', bottom = True  , top = False,
                       left = True, right = True  , labelleft ='on', labelright = 'on') 

    # -- Additional ticks:
    ax.yaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_minor_formatter(NullFormatter())
    # parameters for ticks: (ax, rotation, size)
    tick_rotation_size(ax, rotation, fsize)
    #                                       black                solid            0.5
    ax.grid(True, which = 'major', color = 'grey', linestyle = 'dashed',  alpha = 0.2)  # Grid settings
# ----------------------------------------------------------------------

# 3. simple_line_plot_settings
def simple_line_plot_settings(
        # Input variables:
        ax:plt.Axes,                           # Axis-object of matplotlib-subplots
        plt_settings:dict,                     # User settings
        # Output variables:
    ):                                         # Create figure in output folder
    # -- Local variables:
    ptitle = plt_settings.get('title')
    xlabel = plt_settings.get('xlabel')
    ylabel = plt_settings.get('ylabel')
    xmin   = plt_settings.get('xlims')[0]
    xmax   = plt_settings.get('xlims')[1]
    xstep  = plt_settings.get('xlims')[2]
    ymin   = plt_settings.get('ylims')[0]
    ymax   = plt_settings.get('ylims')[1]
    ystep  = plt_settings.get('ylims')[2]
    fout   = plt_settings.get('output')
    fcol   = 'black'
    fsize  = 14
    fpad   = 20
    output_format = 'png'
    dpi = 300

    # Add legend and plot labels:
    ax.legend()
    ax.set_title( ptitle, color = fcol, fontsize = fsize,      pad = fpad)
    ax.set_xlabel(xlabel, color = fcol, fontsize = fsize, labelpad = fpad)
    ax.set_ylabel(ylabel, color = fcol, fontsize = fsize, labelpad = fpad)
    # Set axes limits:
    ax.set_xticks(np.arange(xmin, xmax, xstep))
    ax.set_yticks(np.arange(ymin, ymax, ystep))
    # Add plot grid:
    plt.grid()
    # Save plot and clean memore:
    plt.savefig(fout, format = output_format, dpi = dpi)
    plt.gcf().clear()

# Section 3: Histograms and Tailor diagram
# ======================================================================

# 1. hist_settings --> User settings for histogram plot_diff_hist
def hist_settings(
        # Input variables:
        ax:plt.Axes,                        # Axis-object of matplotlib-subplots
        plt_title:str,                      # Plot title
        xlabel:str,                         # X axis label
        ylabel:str,                         # Y axis label
        mode:str,                           # Which axis object you want to use (ax1 or ax2)
        # OUTPUT variables:
    ):                                      # Create new figure in output folder
    # -- Local variables:
    fsize = 12  # fontsize
    pad   = 20  # labelpad
    color = 'k' # color

    # -- Set plot title:
    if mode == 'ax1':
        ax.set_title(plt_title, color = color, fontsize = fsize, pad = pad)
    # -- Grid settings:
    ax.grid( True, which = 'major', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    # -- Label settings (x and y):
    if mode == 'ax2':
        # Show x label only for ax2
        ax.set_xlabel(xlabel, color = color, fontsize = fsize, labelpad = pad)
    ax.set_ylabel(    ylabel, color = color, fontsize = fsize, labelpad = pad)
    # -- Settings for ticks (set position for y values)
    ax.tick_params(axis = 'y', which = 'major', pad = pad)
    for label in ax.yaxis.get_ticklabels():
        label.set_horizontalalignment('center')
# ----------------------------------------------------------------------

# 2. plot_diff_hist --> Creation of burned area historgam
def plot_diff_hist(
        # Input variables:
        df:pd.DataFrame,                    # Research dataframe
        ds_name:str,                        # Research parameter
        plt_title:str,                      # Plot title
        xlabel:str,                         # X axis label
        ylabel:str,                         # Y axis label
        ymin:float,                         # Limits for y axis (min)
        ymax:float,                         # Limits for y axis (max)
        path_out:str,                       # Limits for y axis (step)
        # OUTPUT variables:
    ):                                      # Create new figure in output folder
    # -- Create subplots for histogram
    fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 7))
    
    # plot the same data on both axes
    sns.histplot(df, x = "data", hue = "PFT", element = "step", ax = ax )
    sns.histplot(df, x = "data", hue = "PFT", element = "step", ax = ax2) 

    # zoom-in / limit the view to different portions of the data
    ax.set_ylim( 8.0, 12.0)  # outliers only
    ax2.set_ylim(0.0,  4.0)  # most of the data

    ax.set_xlim( ymin, ymax)  # outliers only
    ax2.set_xlim(ymin, ymax)  # most of the data

    # hide the spines between ax and ax2
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.xaxis.tick_top()
    #ax.tick_params(labeltop='off')  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()
        
    d = .010  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)               # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)         # top-right diagonal

    kwargs.update(transform=ax2.transAxes)              # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)        # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # -- Add legend:
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    ax2.legend().set_visible(False)
    # -- Settings for subplots:
    hist_settings(ax , plt_title,  xlabel, ylabel, 'ax1')
    hist_settings(ax2, plt_title,  xlabel, ylabel, 'ax2')
    # -- Save figure and Clean memory:
    plt.savefig(path_out, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()
# ----------------------------------------------------------------------

# 3. Taylor diagram --> Acknowledgment: Yannick Copin for his help
class TaylorDiagram(object):
    """
    Taylor diagram.
    Plot model standard deviation and correlation to reference (data)
    sample in a single-quadrant polar plot, with r=stddev and
    theta=arccos(correlation).
    """

    def __init__(self, refstd,
                 fig=None, rect=111, label='_', srange=(0, 1.5), extend=False):
        """
        Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using `mpl_toolkits.axisartist.floating_axes`.
        Parameters:
        * refstd: reference standard deviation to be compared to
        * fig: input Figure or None
        * rect: subplot definition
        * label: reference label
        * srange: stddev axis extension, in units of *refstd*
        * extend: extend diagram to negative correlations
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist.grid_finder as GF

        self.refstd = refstd            # Reference standard deviation

        tr = PolarAxes.PolarTransform()

        # Correlation labels
        rlocs = np.array([0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1])
        if extend:
            # Diagram extended to negative correlations
            self.tmax = np.pi
            rlocs = np.concatenate((-rlocs[:0:-1], rlocs))
        else:
            # Diagram limited to positive correlations
            self.tmax = np.pi/2
        tlocs = np.arccos(rlocs)        # Conversion to polar angles
        gl1 = GF.FixedLocator(tlocs)    # Positions
        tf1 = GF.DictFormatter(dict(zip(tlocs, map(str, rlocs))))

        # Standard deviation axis extent (in units of reference stddev)
        self.smin = srange[0] * self.refstd
        self.smax = srange[1] * self.refstd

        ghelper = FA.GridHelperCurveLinear(
            tr,
            extremes = (0, self.tmax, self.smin, self.smax),
                        grid_locator1=gl1, tick_formatter1=tf1)

        if fig is None:
            fig = plt.figure()

        ax = FA.FloatingSubplot(fig, rect, grid_helper = ghelper)
        fig.add_subplot(ax)

        # Adjust axes
        ax.axis["top"].set_axis_direction("bottom")   # "Angle axis"
        ax.axis["top"].toggle(ticklabels = True, label = True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].major_ticklabels.set_color("b")
        ax.axis["top"].major_ticklabels.set_size(14)
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")
        ax.axis["top"].label.set_color("b")
        ax.axis["top"].label.set_fontsize(14)

        ax.axis["left"].set_axis_direction("bottom")  # "X axis"
        ax.axis["left"].label.set_text("Normalized Standard Deviation")
        ax.axis["left"].label.set_fontsize(14)
        ax.axis["left"].major_ticklabels.set_color("k")
        ax.axis["left"].major_ticklabels.set_size(14)

        ax.axis["right"].set_axis_direction("top")    # "Y-axis"
        ax.axis["right"].toggle(ticklabels=True)
        ax.axis["right"].major_ticklabels.set_axis_direction(
            "bottom" if extend else "left")
        ax.axis["right"].major_ticklabels.set_color("k")
        ax.axis["right"].major_ticklabels.set_size(14)


        if self.smin:
            ax.axis["bottom"].toggle(ticklabels=False, label=False)
        else:
            ax.axis["bottom"].set_visible(False)          # Unused

        self._ax = ax                   # Graphical axes
        self.ax = ax.get_aux_axes(tr)   # Polar coordinates

        # Add reference point and stddev contour
        l, = self.ax.plot([0], self.refstd, 'b*',
                          ls = '', ms = 16, label = label)
        t = np.linspace(0, self.tmax)
        r = np.zeros_like(t) + self.refstd
        self.ax.plot(t, r, 'k--', label='_')

        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]

    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """
        Add sample (*stddev*, *corrcoeff*) to the Taylor
        diagram. *args* and *kwargs* are directly propagated to the
        `Figure.plot` command.
        """
        l, = self.ax.plot(np.arccos(corrcoef), stddev,
                          *args, **kwargs)  # (theta, radius)
        self.samplePoints.append(l)

        return l

    def add_grid(self, *args, **kwargs):
        """Add a grid."""
        self._ax.grid(*args, **kwargs)

    def add_contours(self, levels = 5, **kwargs):
        """
        Add constant centered RMS difference contours, defined by *levels*.
        """
        rs, ts = np.meshgrid(np.linspace(self.smin, self.smax),
                             np.linspace(0, self.tmax))
        # Compute centered RMS difference
        rms = np.sqrt(self.refstd**2 + rs**2 - 2*self.refstd*rs*np.cos(ts))

        contours = self.ax.contour(ts, rs, rms, levels, **kwargs)

        return contours
# ----------------------------------------------------------------------


# Section 4: NetCDF plots and maps
# ======================================================================

# 1. select_domain --> Settings for research domain used in netcdf_grid and netcdf_grid_series
def select_domain(
        # Input variables:
        domain:str,                       # Research domain
        ax:plt.Axes,                      # Axis-object of matplotlib-subplots
        lons:np.array,                    # 1D array with longitudes
        lats:np.array,                    # 1D array with latitudes
        # OUTPUT variables:
        ) -> tuple[
            plt.Axes,                     # Final plot (Basemap object)
            list[float],                  # Values for meridians
            list[float],                  # Values for parallels.
    ]:
    # -- Select domain:
    if   domain == 'Global':
        m = Basemap(projection = 'moll', resolution  = 'l', lon_0 = 0.0, ax = ax)
        # parameters for parallels and meridians
        params_paral = [ -90.0,  90.0, 30.0]
        params_merid = [-180.0, 180.0, 60.0] 

    elif domain == 'Europe':
        m = Basemap(projection = 'merc', resolution  = 'l'   ,
                    llcrnrlon  =  -11.0, llcrnrlat   =   34.0,
                    urcrnrlon  =   45.0, urcrnrlat   =   72.0,
                    lat_1      =   10.0, lat_2       =   45.0,
                    lon_0      =   20.0, area_thresh = 1000.0,
                    ax         = ax                          )
        # parameters for parallels and meridians
        params_paral = [ 40.0,  80.1, 10.0]
        params_merid = [  0.0,  50.0, 20.0] 

    elif domain == 'Tropics':
        m = Basemap(projection = 'cyl' , resolution  = 'c'   ,
                    llcrnrlon  = -180.0, llcrnrlat   = -23.0 ,
                    urcrnrlon  =  180.0, urcrnrlat   =  23.0 ,
                    ax         = ax                          )
        # parameters for parallels and meridians
        params_paral = [ -15.0,  15.1, 15.0]
        params_merid = [-180.0, 180.0, 90.0]

    elif domain == 'NH':
        m = Basemap(projection = 'cyl' , resolution  = 'c'   ,
                    llcrnrlon  = -180.0, llcrnrlat   = 30.0  ,
                    urcrnrlon  =  180.0, urcrnrlat   = 80.0  ,
                    ax         = ax                          )
        # parameters for parallels and meridians
        params_paral = [  35.0,  80.1, 15.0]
        params_merid = [-180.0, 180.0, 90.0]

    else:
        m = Basemap(projection = 'merc'      , resolution  = 'l'            ,
                    llcrnrlon  = np.min(lons), llcrnrlat   = np.nanmin(lats),
                    urcrnrlon  = np.max(lons), urcrnrlat   = np.max(lats)   ,
                    lat_1      = 40.0        , lat_2       =   45.0         ,
                    lon_0      = 20.0        , area_thresh = 1000.0         ,
                    ax         = ax                                         )
        # parameters for parallels and meridians
        params_paral = [ -90.0,  90.1,  30.0]
        params_merid = [-120.0, 120.1, 120.0]

    return m, params_paral, params_merid
# ----------------------------------------------------------------------

# 2. vis_stations --> create a map with localion of stations
def vis_stations(
        # Input variables:
        data_OUT:str,                     # Output path
        # OUTPUT variables:
    ):                                    # Create new figure in output folder
    # -- Get data for visualization:
    lats = []
    lons = []
    stat = []

    for i in uset.stations:
        lats.append(uset.stations.get(i)[0])
        lons.append(uset.stations.get(i)[1])
        stat.append(uset.stations.get(i)[2])

    plt_title   = 'Geolocation of the random points (robinson projection)'
    output_name = 'STATIONS.png'

    # -- Start Visualization:
    fig  = plt.figure(figsize = (12,7))
    ax   = fig.add_subplot(111) 

    m    = Basemap(projection ='robin', resolution = 'l', lon_0 = 0.0, ax = ax);
    x, y = m(lons, lats)

    m.scatter(x, y, marker = 's', s = 25, color = 'm')
    # -- Parameters for parallels and meridians:
    params_paral = [ -90.0,  90.0, 30.0]
    params_merid = [-180.0, 180.0, 60.0]  
    # -- Draw parallels and  meridians:
    m.drawparallels(np.arange(params_paral[0],
                              params_paral[1],
                              params_paral[2]), labels   = [0, 1, 0, 0],
                                                fontsize = 10          ,
                                                dashes   = [0.3, 2]    )
    m.drawmeridians(np.arange(params_merid[0],
                              params_merid[1],
                              params_merid[2]), labels   = [0, 0, 0, 1],
                                                fontsize = 10          ,
                                                dashes   = [0.3, 2]    )
    # -- Add relief, coastlines and countries:
    m.shadedrelief(scale = 0.2)
    m.drawcoastlines(linewidth = 0.1)
    m.drawcountries(linewidth  = 0.2, color = 'red', linestyle =  '--' )

    # -- Add labels for stations:
    for label, xpt, ypt in zip(stat, x, y):
        plt.text(xpt-750000, ypt+450000, label, fontsize = 10)
    # -- Add plot title:
    plt.title(f'{plt_title}')
    # -- Save figure and clean memory:
    plt.savefig(data_OUT + output_name, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()
# ----------------------------------------------------------------------

# 3. netcdf_grid --> Visualization of 2d array for one moment of time, in different
#                    projections depending on research region.
def netcdf_grid(
        # Input variables:
        axes:plt.Axes,                        # Axis-object of matplotlib-subplots
        domain:str,                           # Research domain (Global, Europe, Tropics, NH, Other)
        lons:np.array,                        # 1D array with longitudes
        lats:np.array,                        # 1D array with latitudes
        data:xr.DataArray,                    # 2D array with actual research parameter (only in one moment of time)
        stat_param:str,                       # Name of statistical parameter (mean, std, trend)
        act_param:str,                        # Reseach parameter (burned_area, npp, gpp, lai, cVeg)
        cbar_limit:list[dict],                # Parametes defenid by users (colormap, y limints)
        ylabel:str,                           # Colorbar label
        plt_title: Optional[str] = None,      # Plot title. Default is None
        ltitle: Optional[bool] = False,       # Do you want to add plot title? Default is False
        lplt_contour: Optional[bool] = False, # Do you want to use contourof or pcolor scheme? Default scheme is
                                              # pcover and lplt_contour is False.
        # OUTPUT variables:
    ) -> plt.Axes:                            # Final plot (Basemap object)

    # -- Define limits for colorbars and settings for legend:
    for item in cbar_limit:
        if (item['mode'] == act_param and item['param'] == stat_param):
            min_value = item['ymin']
            max_value = item['ymax']
            colormap  = item['cbar']
    #           location   pad    size
    if domain in ('Tropics', 'NH'):
        pset = ['bottom', '30%', '10%']
    else:
        pset = ['bottom', '10%', '5%' ]

    # -- Select settings for research domain:
    m, params_paral, params_merid = select_domain(domain, axes, lons = lons,
                                                                lats = lats)
    # -- Create mesh grib based on lat and lon (1d arrays):
    lon, lat = np.meshgrid(lons, lats)
    xi, yi   = m(lon, lat)
    # -- Define parameter for visualization (It should be a 2d array):
    var = maskoceans(lon, lat, data)
    # -- Define method for visualization:
    if lplt_contour == True:
        levels = MaxNLocator(nbins = 12).tick_values(min_value, max_value) 
        cs = m.contourf(xi, yi, var, cmap = colormap, levels = levels, extend = 'both')
    else:
        cs = m.pcolor(  xi, yi, var, cmap = colormap, vmin = min_value ,
                                                      vmax = max_value)
    # -- Add parallels and meridians:
    # labels = [left,right,top,bottom]
    m.drawparallels(np.arange(params_paral[0], params_paral[1], params_paral[2]),
                    labels     = [0, 1, 0, 0], fontsize = 10  , dashes = [0.3, 2])

    if domain != 'Global':
        m.drawmeridians(np.arange(params_merid[0], params_merid[1], params_merid[2]),
                        labels = [0, 0, 0, 1], fontsize = 10  , dashes = [0.3, 2]  )
    # -- Add water objects mask, coastlines and country boundaries:
    m.drawlsmask(land_color = 'coral', ocean_color = 'aqua', lakes = True, alpha = 0.05)
    m.drawcoastlines(linewidth = 0.1)
    m.drawcountries( linewidth = 0.2)
    # -- Add legend:
    cbar = m.colorbar(cs, location = pset[0], label = ylabel, pad  = pset[1],
                                                              size = pset[2])
    # -- Sometimes our values have strange format. Change to scientific format
    if (min_value >= -1e-3 and min_value <= -1e-9):
        cbar.formatter.set_powerlimits((0, 0))
    # -- Add Title
    if ltitle == True:
        plt.title(f'{plt_title}')   
    return m
# ----------------------------------------------------------------------

# 4. netcdf_grid_series --> Visualization of NetCDF data on subplots, in different
#                           projections depending on research region.
def netcdf_grid_series(
        # Input variables:
        domain:str,                       # Research domain (Global, Europe, Tropics, NH, Other)
        years:list[str],                  # The actual year (dates) for research
        row_numbs:int,                    # Numbers of row for subplots
        cols_numbs:int,                   # Numbers of columns for subplots
        lons:np.array,                    # 1D array with actual longitudes
        lats:np.array,                    # 1D array with actual latitudes
        data:xr.DataArray,                # 3D array with actual research parameter (need time steps)
        colormap:str,                     # Color scheme for data
        data_OUT:str,                     # Output path
        plot_title:str,                   # Plot title
        # OUTPUT variables:
    ):                                    # Create new figure in output folder
    # -- Local variables:
    re_range = 1e-9

    # Start function:
    fig = plt.figure(figsize = (14,10))
    # Create grid:
    egrid = (row_numbs, cols_numbs)

    ax_list = []
    for i in range(egrid[0]):
        for j in range(egrid[1]):
            ax_list.append(plt.subplot2grid(egrid, (i, j), rowspan = 1,
                                                           colspan = 1))
    # -- Show data on the subplots:
    for i in range(len(years)):
        # -- Select domain:
        m, params_paral, params_merid = select_domain(domain, ax_list[i], lons = lons,
                                                                          lats = lats)
        # -- Create mesh grib based on lat and lon (1d arrays):
        lon, lat = np.meshgrid(lons, lats)
        xi, yi   = m(lon, lat)

        # -- Define parameter for visualization (It should be a 3d array):
        var = maskoceans(lon, lat, data.sel(time = years[i])[0]) * re_range
        
        # -- Start visualization:
        cs = m.contourf(xi, yi, var, cmap = colormap, extend = 'both')
        # -- Add water objects mask:
        m.drawlsmask(land_color  = 'coral', ocean_color = 'aqua' ,
                     lakes       = True   , alpha       = 0.1    )
        # -- Add titles for each plot:
        plt.title(f'{years[i]}')
        # -- Add legend for each plot:
        colormesh = m.pcolormesh(lon, lat, var, vmin = 0.0, vmax = 1.4, cmap = colormap)

        if domain in ('Tropics', 'NH'):
            #       location        label      pad    size
            pset = ['bottom', '1000km\u00B2', '75%', '25%']
        else:
            pset = ['bottom', '1000km\u00B2', '10%', '2%' ]
            
        cbar = m.colorbar(colormesh, location = pset[0], label = pset[1],
                                         pad  = pset[2], size  = pset[3])
    # -- Add general title for plot:
    if   domain in ('Global', 'Tropics', 'NH') :
        fig.suptitle(f'{plot_title}', fontsize = 16, y = 0.90)    
    else:
        fig.suptitle(f'{plot_title}', fontsize = 16, y = 1.05)
        
    # Save plot and cean memory:
    plt.savefig(data_OUT, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()
# ----------------------------------------------------------------------

# 5. create_fast_xarray_plot --> create 2D maps based on input NetCDF data and
#                                xarray options for visualization (simple plot):
def create_fast_xarray_plot(
        # Input variables:
        pft_data:xr.DataArray,       # Data for visualization
        plt_mode:str,                # key word from plt_settings (e.g.: all_PFT, nat_PFT and ets)
        plt_settings:dict,           # Plot settings
        # OUTPUT variables:
    ):                               # Create new plot in output folder
    # -- Local variables:
    fig_dpi = 300
    fig_format = 'png'
    fig_set = plt_settings.get(plt_mode)

    # -- Create 2D plot:
    fig = plt.figure(figsize = (12,7))
    pft_data.plot(
        robust = fig_set.get('robust'),
        cmap = fig_set.get('colormap'),
        vmin = fig_set.get('vmin'),
        vmax = fig_set.get('vmax'),
        col = fig_set.get('col'),
        col_wrap = fig_set.get('col_wrap'),
    )
    # -- Add plot title
    if plt_mode != 'monthly_diff':
        plt.title(fig_set.get('title'))
    # -- Save figure and clean memory:
    plt.savefig(fig_set.get('output'), format = fig_format, dpi = fig_dpi)
    plt.close(fig)
    plt.gcf().clear()
# ----------------------------------------------------------------------


# Section 5. Special functions for visualization of data COSMO-CLM data
# ======================================================================

# 1. get_params --> Define the observational parameter names
def get_params(
        # Input variables:
        param:str,                   # Name of the research parameter
        # OUTPUT variables:
        ) -> str :                   # Name of the output parameter
                                     # In case of ZVERBO and AEVAP_S input
                                     # parameters, there are 2 output variables
    # -- Define user output names:
    set_param = {
        'ALHFL_S' : 'LE',
        'ASHFL_S' :  'H',
        'T_2M'    : 'T_2M',
        'T_S'     :  'TS' ,
        'TMAX_2M' : 'TMAX',
        'TMIN_2M' :  'TMIN',
        'TOT_PREC': 'TOT_PREC',
        'AEVAP_S' : ['Et_a', 'Et_b'],
        'ZVERBO'  : ['Ep_a', 'Ep_b']
    }
    # -- Get data:
    if param not in ('ZVERBO', 'AEVAP_S'):
        return set_param.get(param)
    else:
        return set_param.get(param)[0], set_param.get(param)[1]
# ----------------------------------------------------------------------

# 2. vis_stat_mode --> The subroutine needs for getting actual parameters for plot
#                      Function is adapted for: get_m, get_2m, get_d, get_u, get_h
def vis_stat_mode(
        # Input variables:
        lst4data:list[pd.DataFrame],          # Datasets with COSMO data (COSMO_CTR, v3.5, v4.5, v4.5e )
        df:pd.DataFrame,                      # Dataset with in-situ, reanalysis, satellite data
        param:str,                            # Parameter from COSMO
        lst4legend:list[str],                 # List with COSMO names
        ylable:str,                           # Label for Y-axis
        y1:float,                             # Limits for y axis (min)
        y2:float,                             # Limits for y axis (max)
        step:float,                           # Limits for y axis (step)
        domain:str,                           # Research territory
        mode:str,                             # Type of the function (get_m, get_2m, get_d, get_u, get_h)
        data_out:str,                         # Output path
        # OUTPUT variables:
    ):                                        # Create new figure in output folder
    # -- Settings for text into figure:
    #        color        title         label 
    #                 size    pad    size    pad
    pset = ['black',   18,    20,     16,    20 ]

    # Settings for plot title:
    if domain == '1':
        #           Domain       Station
        tset = ['Parc'      , 'Rollesbroich']
    elif domain == '2':    
        tset = ['Linden'    , 'Linden'      ]
    else:
        tset = ['Lindenberg', 'Lindenberg'  ]

    # Define observational data for analysis:
    if param not in ('ZVERBO', 'AEVAP_S'):
        var1 = get_params(param)
    else:
        var1, var2 = get_params(param)

    # Create data for visualization (COSMO + observations):
    if param not in ('AEVAP_S', 'ZVERBO'):
        lst4data.extend([df[var1]])      
        lst4legend = lst4legend + ['OBS'] 
    else:
        lst4data.extend([df[var1], df[var2]])
        lst4legend = lst4legend + ['GLEAM_v3.5a', 'GLEAM_v3.5b'  ]  

    # Define line numbers:
    lines_count = len(lst4legend)
    # Visualization:
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    if param != 'TOT_PREC':
        plot = line_plots(ax, lines_count, lst4data, lst4legend, plt_type = 'line_plot')
    else:
        plot = line_plots(ax, lines_count, lst4data, lst4legend, plt_type = 'bar')
    # Settings for legend:
    font = font_manager.FontProperties(family = 'Arial', style  = 'normal', size = 16)
    ax.legend(prop = font, loc = 'upper right')
    # Settings for plot title and labels:
    if mode == 'get_d':
        plt_name    = (f'Daily average values of {param} in June from 2010 to 2015' +
                        '\n\n' + f'Domain: {tset[0]}      Station: {tset[1]}')
    elif mode == 'get_u':
        time_period = '05.07.2011 to 15.07.2011' + '\n\n'
        plt_name    = (f'Hourly values of {param} from {time_period}' +
                       f'Domain: {tset[0]}      Station: {tset[1]}'   )
    elif mode == 'get_h':
        plt_name    = (f'Diurnal cycle of {param} from June to August' + '\n\n' +
                       f'Domain: {tset[0]}      Station: {tset[1]}'             )
    else:
        plt_name    =  f'Domain: {tset[0]}      Station: {tset[1]}'

    ax.set_title(plt_name, color = pset[0], fontsize = pset[1], pad = pset[2])
    # -- Settings for axis (x and y) + labels:
    # Only when x axis is active
    if mode == 'get_d' or mode == 'get_u' or mode == 'get_h':
        if mode == 'get_d':
            ax.set_xticks(np.arange(0, 30.1, 5))
            xlabel = 'Day of month'
        elif mode == 'get_u':
            xlabel = 'Date'
        else:
            ax.set_xticks(np.arange(0, 24.1, 3))
            xlabel = 'Hour'     
        ax.set_xlabel(xlabel, color = pset[0], fontsize = pset[3], labelpad = pset[4])
    # y axis is active always
    ax.set_ylabel(    ylable, color = pset[0], fontsize = pset[3], labelpad = pset[4])
    ax.set_yticks(np.arange(y1, y2, step))
    # parameters for ticks: rotation, size
    tick_rotation_size(ax, 30, 16)
    # Add grid
    plt.grid()
    # Plot save
    pout_set = {'get_m' : data_out + f'Annual/{param}_annual.png',
                'get_2m': data_out +        f'{param}_annual.png',
                'get_d' : data_out + f'Monthly/{param}_June.png' ,
                'get_u' : data_out + f'Weekly/{param}_verif.png' ,
                'get_h' : data_out + f'Diurnal/{param}_Hour.png' }
    plt.savefig(pout_set.get(mode), format = 'png', dpi = 300)
    # Clean memory
    plt.close(fig)        
    plt.gcf().clear() 
# ----------------------------------------------------------------------

# 3. get_data_m -->
def get_data_m(
        # Input variables:
        ax:plt.Axes,                      # Axis-object of matplotlib-subplots
        csr:pd.DataFrame,                 # COSMO data (COSMO_CTR)
        cs35:pd.DataFrame,                # COSMO data (COSMO_v3.5)
        cs45:pd.DataFrame,                # COSMO data (COSMO_v4.5)
        cs45e:pd.DataFrame,               # COSMO data (COSMO_v4.5e)
        gla:pd.DataFrame,                 # GLEAM v3.5a data
        glb:pd.DataFrame,                 # GLEAM v3.5b data
        df_obs:pd.DataFrame,              # In-situ data (FLUXNET, EURONET)
        param:str,                        # Parameter name from COSMO
        ylabel:str,                       # Label for Y-axis
        input_region:str,                 # Research domain
        y1:float,                         # Limits for y axis (min)
        y2:float,                         # Limits for y axis (max)
        step:float,                       # Limits for y axis (step)
        time_step:str,                    # Time period for x axis
        xtext:list[str],                  # Additional time intervals
        xset: Optional[bool] = True,      # Settings special for x axis
        legendary: Optional[bool] = True  # Settings for legend
        # OUTPUT variables:
    ):                                    # Create new figure in output folder
    # -- Define special location for xticks:
    #                                  main ticks                         minor ticks
    xsettings = {'1D'    : [np.arange(0, len(csr) + 1, 31), np.arange(14  , len(csr) + 1, 31)],
                 '2D'    : [np.arange(0, len(csr) + 1, 15), np.arange( 7.5, len(csr) + 1, 15)],
                 '5D'    : [np.arange(0, len(csr) + 1,  6), np.arange( 3  , len(csr) + 1,  6)],
                 'Other' : [np.arange(0, len(csr)    ,  1), np.arange( 0  , len(csr)    ,  1)]}

    x_main = xsettings.get(time_step)[0]
    x_add  = xsettings.get(time_step)[1]

    # -- Create lists for: data, labels, colors, linestile:
    lst4data  = [csr      , cs35      , cs45      , cs45e      ]
    lst4label = ['CCLMref', 'CCLMv3.5', 'CCLMv4.5', 'CCLMv4.5e']
    lst4color = ['blue'   , 'green'   , 'brown'   , 'red'      ]
    lst4style = ['-'      , '-'       , '-'       , '-'        ]

    # -- Visualization
    for i in range(len(lst4data)):
        ax.plot(
            lst4data[i].index,
            lst4data[i],
            label = lst4label[i],
            color = lst4color[i],
            linestyle = lst4style[i])

    if param in ('AEVAP_S', 'ZVERBO'):
        ax.plot(gla.index, gla, label = 'GLEAM v3.5a', color = 'black', linestyle = ':' )
        ax.plot(glb.index, glb, label = 'GLEAM v3.5b', color = 'black', linestyle = '--')
    elif param in ('T_2M', 'T_S', 'TMAX_2M', 'TMIN_2M'):
        ax.plot(df_obs.index , df_obs , label = 'OBS', color = 'black', linestyle = ':' )

    # -- Settings for plot:
    # 3.1. Add legend
    if legendary == True:
        font = font_manager.FontProperties(family = 'Arial', style  = 'normal', size = 14)
        ax.legend(prop = font, loc = 'upper center', bbox_to_anchor = (0.5, 2.5),
                  ncol = 6   , fancybox = True     , shadow = False)

    # 3.2. Set y-axis    
    ax.set_ylabel(ylabel, color = 'black', fontsize = 14, labelpad = 50)       # y label
    ax.set_yticks(np.arange(y1, y2, step))                                     # y values 

    ax.tick_params(axis ='y'  , which ='major', bottom    = True, top = False, # y ticks main 
                   left = True, right = True  , labelleft ='on' , pad = 30   ,
                   labelright = 'on')

    ax.tick_params(axis ='y'  , which ='minor', bottom    = True, top = False, # y ticks minor
                   left = True, right = True  , labelleft ='on' , pad = 30   ,
                   labelright = 'on')

    # 3.3. Set x-axis
    ax.set_xticks(x_main)
    ax.xaxis.set_major_formatter(ticker.NullFormatter())  # don't show main x values

    if xset == True: 
        # Set special x values and ticks
        ax.xaxis.set_minor_locator(ticker.FixedLocator([
            x_add[0], x_add[1], x_add[2], x_add[3], x_add[4], x_add[5]]))

        ax.xaxis.set_minor_formatter(ticker.FixedFormatter([
            xtext[0], xtext[1], xtext[2], xtext[3], xtext[4], xtext[5]]))

        ax.tick_params(axis = 'both', which = 'minor', labelsize = 16)

    tick_rotation_size(ax, 30, 14)     # parameters for ticks (ax, rotation, size)
    ax.grid()                          # Get grid
# ----------------------------------------------------------------------

# 4. plot_waves -->  Create plot with information about heat and cold waves
def plot_waves(
        # Input variables:
        ts_main:pd.Series,                 # Timeseries with all data
        ts_hot:pd.Series,                  # Timeseries with extrem hot periods
        ts_cold:pd.Series,                 # Timeseries with extrem cold periods
        interval:str,                      # Time period
        domain:str,                        # Research domain
        station:str,                       # Research station
        x_start:str,                       # First date of time period
        x_stop:str,                        # Last day of time period
        data_exit:str,                     # Output path
        cosmo_type:bool,                   # Do you use COSMO data?
        # OUTPUT variables:
    ):                                     # Create new figure in output folder
    # -- Local settings for plot:
    fcol   = 'black'
    fsize  = 14
    fpad   = 20
    ptitle = (f'Heat and cold waves {interval} \n\n Domain: {domain}     Station: {station}')
    xlabel = 'Standart deviation'
    ylabel = 'Years'

    # Visualization
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    if cosmo_type is True:
        plt.plot(ts_main.index, ts_main, label = 'T2_M COSMO', color = 'b', linestyle = '-')
    else:
        plt.plot(ts_main.index, ts_main, label = 'T2_M HYRAS', color = 'g', linestyle = '-')
    plt.scatter(ts_hot.index  , ts_hot , label = 'hot wave'  , color = 'r', linewidths = 2 )
    plt.scatter(ts_cold.index , ts_cold, label = 'cold wave' , color = 'm', linewidths = 2 )

    # Plot settings   
    ax.set_title( ptitle, color = fcol, fontsize = fsize,      pad = fpad)
    ax.set_ylabel(xlabel, color = fcol, fontsize = fsize, labelpad = fpad)
    ax.set_xlabel(ylabel, color = fcol, fontsize = fsize, labelpad = fpad)

    ax.set_xticks(pd.date_range(x_start, x_stop, freq = '2M')) #'2MS')) #freq = 'YS'))
    ax.set_yticks(np.arange(-2.5, 2.51, 0.5))

    # parameters for ticks: rotation, size
    tick_rotation_size(ax, 90, 14)

    # Get grid and legend
    plt.grid()
    ax.legend(loc = 'lower right', frameon = True)

    # Save figure
    if cosmo_type == True: 
        out_path = data_exit + f'Waves_{interval} COSMO.png'
    else:
        out_path = data_exit + f'Waves_{interval} HYRAS.png'
    plt.savefig(out_path, format = 'png', dpi = 300)
# ----------------------------------------------------------------------
