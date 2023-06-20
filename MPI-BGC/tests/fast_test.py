# -*- coding: utf-8 -*-
"""
Script for testing burned area ESA-CCI MODISv5.1 data

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-10-17 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-14 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project 
    1.3    2023-02-13 Evgenii Churiulin, MPI-BGC
           Updated output variables and data for functions (get_path_in)
    1.4    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     =================
# -- Standard:
import os
import sys
import pandas as pd
import xarray as xr
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4xarray import comp_area_lat_lon
from libraries.lib4sys_support import makefolder
from libraries.lib4upscaling_support import get_upscaling_ba, get_upscaling_ba_veg_class
from calc.vis_controls import one_plot
from settings.path_settings import get_path_in, output_path
from libraries.lib4visualization import netcdf_line_plots as nlplot
from libraries.lib4visualization import simple_line_plot_settings

# =============================   Personal functions   =================

# yearsum --> Get annual values
def yearsum(data):
    return data.sum(dim = {'lat', 'lon'}).groupby('time.year').sum()

# get_ocn --> reading OCN NetCDF data:
def get_ocn(
        # Input variables:
        path:str,                # Input path
        var:str,                 # Research variable
        # Output variables:
    ) -> tuple[xr.DataArray,     # Annual OCN data
               xr.DataArray]:    # Original OCN data

    nc = (xr.open_dataset(path, decode_times = False)
            .assign_coords({'time': pd.date_range('2000-01-01', '2021-01-01',
                                                              freq = '1M'  )}))   
    # Add field with pixel area: 
    nc = nc.assign(xr.Dataset({'area': (('lat', 'lon'),                         
                      comp_area_lat_lon(nc.lat.values,
                                        nc.lon.values))}, 
                      coords = {'lat' : nc.lat.values, 
                                'lon' : nc.lon.values})) 
    # Data from TRENDY    
    nc[var] = nc[var].sum(dim = {'vegtype'})                                   
    nc[var] = nc[var] * nc['area'] * rec_coef * nc[var].time.dt.days_in_month

    tba_ocn   = yearsum(nc[var]) 
    orig_data = nc[var]
    return tba_ocn, orig_data

# =============================   User settings   ======================
# -- Logical parameteres:
# Do you want to create plot for comparison burned area?
lplot_1 = True
# Do you want to create plot for comparison burned area by PFT?
lplot_2 = True
# Do you want to create plot for comparison burned area and burned area by PFT?
lplot_3 = True

# -- Get output paths and create folder for results:
pout = makefolder(output_path().get('fast_test'))
print(f'Your data will be saved at {pout}')

# -- Define user settings for linear plots:
user_line_settings = {
    'plot_1' : {
        'labels' : ['BA - 720*1440', 'BA - 360*720'],
        'colors' : ['b', 'r'],
        'styles' : ['-', '-.'],
        'title'  : 'Comparison BA ESA-CCI MODIS data',
        'xlabel' : 'Years',
        'ylabel' : 'Burned area 1000 km2',
        'xlims'  : [ 2000, 2021  , 2  ],
        'ylims'  : [ 2000, 6000.1, 500],
        'output' : pout + 'BA.png',
    },
    'plot_2' : {
        'labels' : ['BA_PFT_all - 720*1440', 'BA_PFT_all - 360*720', 'BA_PFT_nat - 360*720', 'BA_OCN - 360*720'],
        'colors' : ['b', 'r' , 'g' , 'm' ],
        'styles' : ['-', '-.', '-.', '--'],
        'title'  : 'Comparison BA ESA-CCI MODIS data by PFT',
        'xlabel' : 'Years',
        'ylabel' : 'Burned area 1000 km2',
        'xlims'  : [ 2000, 2021  , 2  ],
        'ylims'  : [ 2000, 6000.1, 500],
        'output' : pout + 'BA_PFT.png',
    },
    'plot_3' : {
        'labels' : ['BA', 'BA_PFT'],
        'colors' : ['b', 'r'],
        'styles' : ['-', '-.'],
        'title'  : 'Comparison BA and BA_PFT ESA-CCI MODIS data',
        'xlabel' : 'Years',
        'ylabel' : 'Burned area 1000 km2',
        'xlims'  : [ 2000, 2021  , 2  ],
        'ylims'  : [ 2000, 6000.1, 500],
        'output' : pout + 'BA2BA_PFT.png',
    },
}
# -- Recalculation coefficient:
rec_coef = 1e-9
# -- Don't change this parameters:
esa_var1 = 'burned_area'
esa_var2 = 'burned_area_in_vegetation_class'
esa_pft_var = 'vegetation_class'
# -- User time limit for global maps (should be simular for ESA-CCI MODIS and OCN)
year_start = '2002-01-01'
year_stop  = '2016-01-01'
# -- Natura PFT starts from ... (index ESA-CCI MODIS PFTs):
natur_pft = 3
# =============================    Main program   =======================
if __name__ == '__main__':
    print('START program')
    # -- Get input:
    esa_pin, esa_param = get_path_in(['BA_MODIS'], esa_var1)
    ocn_pin, ocn_param = get_path_in(['OCN_S2Diag'], 'firepft')

    # -- Reading ESA-CCI data:
    ncfile = xr.open_dataset(esa_pin[0])
    ncfile = ncfile.assign(xr.Dataset({'area': (('lat', 'lon'),
                              comp_area_lat_lon(ncfile.lat.values,
                                                ncfile.lon.values))},
                              coords = {'lat' : ncfile.lat.values,
                                        'lon' : ncfile.lon.values}))
    ncfile[esa_var1] = ncfile[esa_var1] * rec_coef
    ncfile[esa_var2] = ncfile[esa_var2] * rec_coef
    # -- Reading OCN data:
    tba_ocn, tba_ocn_data = get_ocn(ocn_pin[0], 'burnedArea')

    # -- Get burned area plot based on ESA-CCI MODIS data:
    tba_720_1440 = yearsum(ncfile[esa_var1])
    tba_360_720 = yearsum(get_upscaling_ba(ncfile, esa_var1))
    # Plot 1: Get gata presented on different grids (BA - 720-1440 and BA 360-720)
    if lplot_1 is True:
        # Add data to a visualization list:
        lst4data = [tba_720_1440, tba_360_720]
        pic_lplot = nlplot(
            len(lst4data),
            lst4data,
            user_line_settings.get('plot_1').get('labels'),
            user_line_settings.get('plot_1').get('colors'),
            user_line_settings.get('plot_1').get('styles'),
            False,
        )
        # Apply user settings for linear plot:
        simple_line_plot_settings(pic_lplot, user_line_settings.get('plot_1'))

    # -- Get burned area plot based on ESA-CCI and OCN PFTs:
    # Get annual ESA-CCI PFTs (original grid - 1440*720):
    tba_pft_720_1440 = yearsum(ncfile[esa_var2].sum(dim = {esa_pft_var}))
    if lplot_2 is True:
        # ESA-CCI PFTs (OCN grid - 720*300):
        ba_pft_360_720  = get_upscaling_ba_veg_class(ncfile, esa_var2)
        # Get total burned area based on PFT
        tba_pft_360_720     = yearsum(ba_pft_360_720.sum(dim = {esa_pft_var}))
        # Select natural ESA-CCI PFT:
        nat_tba_pft_360_720 = ba_pft_360_720[:, natur_pft:, :,:].sum(dim = {esa_pft_var})
        # get sum of natural PFT
        tba_pft_360_720_nat = yearsum(nat_tba_pft_360_720)
        # -- Plot 2:
        # Add data to a visualization list:
        lst4data = [tba_pft_720_1440, tba_pft_360_720, tba_pft_360_720_nat, tba_ocn]
        # Plot 2: Linear plot with ESA-CCI PFT data + OCN PFT:
        pic_lplot = nlplot(
            len(lst4data),
            lst4data,
            user_line_settings.get('plot_2').get('labels'),
            user_line_settings.get('plot_2').get('colors'),
            user_line_settings.get('plot_2').get('styles'),
            False,
        )
        # Apply user settings for linear plot:
        simple_line_plot_settings(pic_lplot, user_line_settings.get('plot_2'))
        # -- Get data for GLOBAL MAP:
        # Get time mean values for ESA-CCI MODIS natural PFT:
        nat_tba_pft_360_720 = (
            # Get annual values from monthly:
            nat_tba_pft_360_720.resample(time = 'A').sum('time')
            # Select data over time and geographical coordinates:
                               .sel(time = slice(year_start, year_stop),
                                    lat = slice(  90.0,  -60.0),
                                    lon = slice(-180.0,  180.0))
            # Get mean values over years:
                                .mean(['time'])
        )
        # Get OCN data:
        tba_ocn_data = (
            # Get annual values from monthly:
            tba_ocn_data.resample(time = 'A').sum('time')
            # Select data over time
                        .sel(time = slice(year_start, year_stop))
            # Get mean values over years:
                        .mean(['time'])
        )
        # Get difference (ESA-CCI - OCN):
        diff = nat_tba_pft_360_720 - tba_ocn_data

        lst4dsnames = ['MODIS', 'OCN', 'DIFF']
        lst4data = []
        lst4data.extend([nat_tba_pft_360_720, tba_ocn_data, diff])
        # Get latitude and longitute values:
        lst4lat  = []
        lst4lon  = []
        for i in range(len(lst4data)):
            lst4lat.append(lst4data[i].lat.values)
            lst4lon.append(lst4data[i].lon.values)
        # a. Get output settings for MEAN plots
        m_title    = []   # list of plot names - mean
        m_path_OUT = []   # list of output paths
        for ds_name in lst4dsnames:
            m_title.append(f'MEAN values in {ds_name}')
            m_path_OUT.append(pout + f'2D_map4{ds_name}.png')
        # b. Get MEAN plot:
        one_plot(
            lst4dsnames,
            'mean',
            'Global',
            lst4lon,
            lst4lat,
            lst4data,
            esa_var1,
            esa_var1,
            m_title,
            m_path_OUT,
        )
    # -- Comparison burned area and burned area by PFT values:
    if lplot_3 is True:
        lst4data = [tba_720_1440, tba_pft_720_1440]
        pic_lplot = nlplot(
            len(lst4data),
            lst4data,
            user_line_settings.get('plot_3').get('labels'),
            user_line_settings.get('plot_3').get('colors'),
            user_line_settings.get('plot_3').get('styles'),
            False,
        )
        # Apply user settings for linear plot:
        simple_line_plot_settings(pic_lplot, user_line_settings.get('plot_3'))
# =============================    End of program   ====================
