# -*- coding: utf-8 -*-
"""
Script for reading NetCDF files with information about fire or burned area

How to use this script: 
    1. You have to open user_settings from settings folder and set your settings.
       Most parameters in "User settings" depend on user_settings;

    2. Pay attention to section 1.2 - Settings for research domain and parameter.
       If you want to use automatically post processing for all domains and regions
       them you have to adapt your run_ocn_postprocessing.sh. Otherwise, 
       parameters (region and param_var) should be uncommented. 

    3. Pay attention to section 1.4 - Get input paths and NetCDF attributes
       Actual information about datasets are available in path_settings 

    4. Check your settings for actual NetCDF attributes, labels and ets. You can
       get your NetCDF settings in section 2.1

    5. Check your settings for 1D, 2D and 3D plots. Section 2.2. You can change
       plot settings in user_settings, also if you want to change colors for 
       linear plots - you should change lib4colors from libraries.

If you want to add new dataset:
    1. Add new dataset into mcluster_set or mlocal_set files;
    2. Check your dataset settings in path_settings. If everything is fine, go next;
    3. Add new dataset into user_settings. In particular you have add changes in:
        a. Section - 1.4: Select available datasets (OCN simulations and datasets)
        b. Section - 1.4.3 Select all datasets.
        c. Section - 1.4.4 Datasets have different time perios.
        d. Section - 1.5 Settings for difference metrics (diff = refer - comp_ds)
    4. Add new dataset into lib4colors 
    5. Add or check algorithm for data reading into lib4xarray - function get_data.
    6. You can run this script

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de


History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-06-10 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-28 Evgenii Churiulin, MPI-BGC
           Release 2. The script structure was updated. All functions were
           adapted to the new versions of modules
    1.3    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project 
    1.4    2023-02-13 Evgenii Churiulin, MPI-BGC
           1 - Added new option for running. Now, you can use shell script 
           run_ocn_postprocessing.sh with domains and research parameters or you
           can uncoment parameters (region and param_var) for manual post processing
           2 - res_param was udapted, due to changes in path_settings 
    1.5    2023-05-22 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
# 1.1: Standard modules
import os
import sys
import warnings
warnings.filterwarnings("ignore")

# 1.2 Personal module
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4xarray import get_data, get_interpol, annual_mean
from libraries.lib4sys_support import makefolder
from settings import user_settings as uset
from settings import path_settings as pset
from calc.one_point import one_point_calc
from calc.vis_controls import one_linear_plot, one_plot, collage_plot
from calc.stat_controls import timmean, timstd, timtrend, get_difference
# =============================   Personal functions   ==================

# ================   User settings (have to be adapted)  ================

# -- Logical parameteres (All parameter you can choose at user_settings):
lnc_info        = uset.logical_settings[1]    # Do you want to get more information about data?
station_mode    = uset.logical_settings[2]    # Do you want to get values for stations
lvis_lines      = uset.logical_settings[3]    # Do you want to visualize data (line plots)
lBasemap_moment = uset.logical_settings[4]    # Do you want to visualize data on grid for one moment?
lmodis_nat      = True                        # Use natural PFT or all

# -- Settings for research domain and parameter:
#    You can run this script manually for your research domain and parameter or
#    you can set them in run_ocn_postprocessing.sh script.

# -- Manual mode (uncomment these lines):
#region    = 'Global'      # Research domain
#param_var = 'burned_area' # Research parameter

# -- Automatic mode (uncomment these lines)
region     = sys.argv[1] # Research domain
param_var  = sys.argv[2] # Research parameter

print('Actual research domain - fire_xarray:',region)
print('Actual research parameter - fire_xarray:', param_var)

# -- Format of output figures:
plt_format = uset.form4out_fig

# -- Get datasets and time perios for them (satellite + ocn):
lst4dsnames = uset.av_datasets.get(param_var)

# -- Get input paths and NetCDF attributes:
ipaths, res_param = pset.get_path_in(lst4dsnames, param_var)
if lmodis_nat == True: 
    for i in range(len(lst4dsnames)):
        if lst4dsnames[i] == 'BA_MODIS':
            tmp_path, tmp_res_param = pset.get_path_in([lst4dsnames[i]], 'burned_area_nat')
            ipaths[i]    = tmp_path[0]
            res_param[i] = tmp_res_param[0]

# -- Get output paths and create folder for results:
data_OUT = pset.output_path().get('fire_xarray')
data_OUT = makefolder(data_OUT + f'/{param_var}')
print(f'Your data will be saved at {data_OUT}')

#==============================================================================
# 2.  Additional parameters - User settings (if you want you can change it,
#     but the program can work with the actual parameters without changes)
#==============================================================================
  
# 2.1: Get initial parameters for research datasets
#------------------------------------
#   1. svname    - Short name of the parameter
#   2. lvname    - Full  name of the parameter
#   3. lp_units  - Units for 2D plots
#   4. cp_units  - Units for 3D plots 
svname, lvname, lp_units, cp_units = pset.get_parameters(lst4dsnames, param_var) 

# 2.3: Case: lBasemap_moment = TRUE
if lBasemap_moment == True:
     # 2.3.1 Define parameters for calculations:
    lmean_calc  = uset.calculation_settings[0]             # use mean algorithm?
    lstd_calc   = uset.calculation_settings[1]             # use std algorithm?
    ltrend_calc = uset.calculation_settings[2]             # use trends algorithm?
    ldifference = uset.calculation_settings[3]             # use diff algorithm?
    # 2.3.2 Define algorithms for visualization: 
    lmean_plot  = uset.calculation_settings[4]             # plot mean?  (one figure)
    lstd_plot   = uset.calculation_settings[5]             # plot std?  (one figure)
    ltrend_plot = uset.calculation_settings[6]             # plot treand?  (one figure)
    lcollage    = uset.calculation_settings[7]             # plot collage?
                                                           # (1st row - mean, 2nd row - std, 3rd  row - trend)
    ldiff_plot  = uset.calculation_settings[8]             # plot diff. collage?
                                                           # (1st row - mean, 2nd row - std, 3rd  row - trend)
    # Define y axis labal for all figures (plots):
    bm_ylabel   = f'{svname}, {cp_units}'
    # FIRST and LAST year (need for title and output data):
    frs_yr      = uset.time_limits.get(param_var).get('OCN')[0]
    lst_yr      = uset.time_limits.get(param_var).get('OCN')[1]

    # 1.5 Define datasets for difference metrics (diff = refer - comp_ds) 
    if ((lBasemap_moment == True) and (ldifference == True)):
        refer   = uset.diff_options.get(param_var)[0]
        comp_ds = uset.diff_options.get(param_var)[1]
        print('Set datsets for calculating difference (diff = refer - comp_ds)')
        print('Actual refer'  , refer)
        print('Actual comp_ds', comp_ds)

        # Fast control: Check datasets (refer and comp_ds) in lst4dsnames
        if ((refer in lst4dsnames) and (comp_ds in lst4dsnames)):
            print('Reference and experiment datasets are in lst4dsnames \n')
        else:
            print('There are no datasets (reference or experiment) in lst4dsnames.'
                  ' Please, correct data in user_settings \n')
            sys.exit()

# =============================    Main program   =======================
if __name__ == '__main__':
    print('START program')
    lst4data = get_data(ipaths, lst4dsnames, param_var, res_param)              # Get initial data from NetCDF
    lst4data = get_interpol(lst4data, lst4dsnames, region, param_var)           # Convert data to one grid size (upscalling or interpolation)

    # -- Calculations and Visualization:
    # 4.1 Get one point data
    if station_mode == True and region == 'Global':
        print(f'One point mode - domain {region} \n')
        points_test = one_point_calc(
            lst4dsnames, lst4data, param_var, lvname, svname, data_OUT, region)
    else:
        print('Function for calculation and visualization of data for stations was turn off \n')

    # 4.2 Line plots
    if lvis_lines == True:
        # 4.2.1: Get annual plot
        user_plt_settings = {
            'title'       : f'{lvname} over {region} region ',                  # plot title
            'ylabel'      : f'{svname}, {lp_units}'          ,                  # y axis label
            'output_name' : f'{svname}_{region}.{plt_format}',                  # output plot name
            'legend_pos'  : 'upper left'                     }                  # Position of the legend} upper - lower

        # 4.2.2: Get annual mean data
        print('Annual sum / mean values: \n')
        amean = annual_mean(lst4data, param_var)
        one_linear_plot(
            lst4dsnames, region , param_var, amean, user_plt_settings, data_OUT)
    else:
        print('Function for visualization of annual data was turn off \n')

    # -- 2D Map - One moment:
    if lBasemap_moment == True:
        # -- Get data for plots
        # -- Get actual latitudes and longitudes for each dataset:
        lst4lat  = []
        lst4lon  = []
        for i in range(len(lst4data)):
            lst4lat.append(lst4data[i].lat.values)
            lst4lon.append(lst4data[i].lon.values)

        # -- Mean calculations and visualization:
        if lmean_calc == True:
            lst4mean = timmean(lst4dsnames, lst4data, param_var)
            if lmean_plot == True:
                # a. Get output settings for MEAN plots (titles, output_paths)
                m_title    = []
                m_path_OUT = []
                for ds_name in lst4dsnames:
                    m_title.append(f'Mean annual {lvname} over {region} region \n'
                                   f'based on {ds_name} ({frs_yr} - {lst_yr})')
                    m_path_OUT.append(data_OUT +
                                      f'Mean_{svname}_{ds_name}_{region}.{plt_format}')
                # b. Get MEAN plot
                one_plot(
                    lst4dsnames, 'mean', region, lst4lon, lst4lat, lst4mean,
                    param_var, bm_ylabel, m_title, m_path_OUT,
                )
        # -- Standart deviation calculations and visualization:
        if lstd_calc  == True:
            lst4std  = timstd(lst4dsnames, lst4data, param_var)
            if lstd_plot == True:
                # a. Get output settings for STD plots (titles, output_paths)
                s_title    = []
                s_path_OUT = []
                for ds_name in lst4dsnames:
                    s_title.append(f'STD in {lvname} over {region} region '
                                   f'based on {ds_name} ({frs_yr} - {lst_yr})')
                    s_path_OUT.append(data_OUT +
                                      f'STD_{svname}_{ds_name}_{region}.{plt_format}')
                # b. Get STD plot
                one_plot(
                    lst4dsnames, 'std', region, lst4lon, lst4lat, lst4std,
                    param_var, bm_ylabel, s_title, s_path_OUT,
                )
        # -- Time trend calculations and visualization:
        if ltrend_calc == True:
            lst4trends = timtrend(lst4dsnames, lst4data, param_var)
            if ltrend_plot == True:
                # a. Get output settings for TREND plots (titles, output_paths)
                t_title    = []
                t_path_OUT = []
                for ds_name in lst4dsnames:
                    t_title.append(f'Trend in {lvname} over {region} region '
                                   f'based on {ds_name} ({frs_yr} - {lst_yr})')
                    t_path_OUT.append(data_OUT +
                                      f'TREND_{svname}_{ds_name}_{region}.{plt_format}')
                one_plot(
                    lst4dsnames, 'trend', region, lst4lon, lst4lat, lst4trends,
                    param_var , bm_ylabel, t_title, t_path_OUT,
                )

        # -- Get Collage plot (mean, std, trend):
        if lcollage == True:
            print(f'Collage mode - Plot data for {region} region')
            # Create plot
            c_title    = f'Comparison {lvname} over {region} region ({frs_yr} - {lst_yr}):'
            c_path_OUT = data_OUT + f'Collage_{svname}_{region}.{plt_format}'

            collage_plot(
                lst4dsnames,       # datasets
                region,            # region
                lst4lon,           # lon
                lst4lat,           # lat
                lst4mean,          # mean data
                lst4std,           # std data
                lst4trends,        # trend data
                param_var,         # parameter
                bm_ylabel,         # y label
                c_title,           # plot title
                c_path_OUT,        # output path
                ldiff = False,     # diff mode = False
            )
        # -- Get plot with difference (Refer - simulation):
        if ldifference == True:
            # -- Get values for difference (mean, std, trend):
            lst4comp_mean  = get_difference(lst4dsnames, refer, comp_ds, lst4mean)
            lst4comp_std   = get_difference(lst4dsnames, refer, comp_ds, lst4std)
            lst4comp_trend = get_difference(lst4dsnames, refer, comp_ds, lst4trends)

            lst4lon = []
            lst4lat = []
            for i in range(len(lst4comp_mean)):
                lst4lon.append(lst4comp_mean[i].lon.values)
                lst4lat.append(lst4comp_mean[i].lat.values)
            if ldiff_plot == True:
                print(f'Difference mode - Plot data for {region} region')
                # -- Create plot:
                dif_title    = (f'Difference ({refer} - {comp_ds}) in {svname} '
                                f'over {region} region ({frs_yr} - {lst_yr})')
                dif_path_OUT = (data_OUT +
                                f'Diff_{svname}_{refer}_{comp_ds}_{region}.{plt_format}')
                collage_plot(
                    lst4comp_mean,     # datasets
                    region,            # region
                    lst4lon,           # lon
                    lst4lat,           # lat
                    lst4comp_mean,     # mean data
                    lst4comp_std,      # std data
                    lst4comp_trend,    # trend data
                    param_var,         # parameter
                    bm_ylabel,         # y label
                    dif_title,         # title
                    dif_path_OUT ,     # path out
                    ldiff = True,      # diff mode = True
                    refer = refer ,    # reference dataset
                    comp_ds = comp_ds, # dataset for comparison
                )
    else:
        print('Function for visualizing MEAN, STD or TRENDS values'
              ' from NetCDF on the grid was switched off \n')
    print('END program')
# =============================    End of program   =====================
