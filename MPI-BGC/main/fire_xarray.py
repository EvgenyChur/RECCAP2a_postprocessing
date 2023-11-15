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
    1.6    2023-11-13 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
import warnings
warnings.filterwarnings("ignore")

from settings import (logical_settings, lcalc_settings, config, get_settigs4_annual_plots,
    get_settings4maps, get_path_in, get_output_path, get_settings4ds_time_limits,
    get_settings4diff_data, get_parameters)
from libraries import makefolder, get_data, get_interpol, annual_mean
from calc import Statistic, one_point_calc, one_linear_plot, one_plot, collage_plot
# =============================   Personal functions   ==================

def plt_title_and_output_name(
    dsnames:list[str], pout:str, **kwargs) -> tuple[list[str], list[str]]:
    """Create user lists with information about plot title and output names:"""
    # -- Local variables:
    ptf = 'png'
    stp = kwargs.get('stat_param') if 'stat_param' in kwargs else 'NOT_STAT_PARAM'
    lvn = kwargs.get('long_name')  if 'long_name'  in kwargs else 'NOT_SET_LVNAME'
    svn = kwargs.get('short_name') if 'short_name' in kwargs else 'NOT_SET_SVNAME'
    reg = kwargs.get('region') if 'region' in kwargs else 'NOT_SET_REGION'
    yr1 = kwargs.get('frs_yr') if 'frs_yr' in kwargs else 1980
    yr2 = kwargs.get('lst_yr') if 'lst_yr' in kwargs else 2025
    ref = kwargs.get('ds4refer') if 'ds4refer' in kwargs else 'NOT_SET_REFER'
    comp = kwargs.get('ds4comp') if 'ds4comp'  in kwargs else 'NOT_SET_DS_COMP'
    # -- Create lists (in caseL COLLAGE and  DIFF create only 2 str values):
    if stp in ('MEAN', 'STD', 'TREND'):
        title = [
            f'{stp} in {lvn} over {reg} region based on {nds} ({yr1} - {yr2})'
            for nds in dsnames]
        path_OUT = [pout + f'{stp}_{svn}_{nds}_{reg}.{ptf}' for nds in dsnames]
    # -- Collage plot case:
    elif (stp == 'COLLAGE'):
        title = f'Comparison {lvn} over {reg} region ({yr1} - {yr2}):'
        path_OUT = pout + f'Collage_{svn}_{reg}.{ptf}'
    # -- Difference plot
    elif (stp == 'DIFF'):
        title = (
            f'Difference ({refer} - {comp_ds}) in {svname} '
            f'over {region} region ({yr1} - {yr2})')
        path_OUT = (pout + f'Diff_{svn}_{ref}_{comp}_{reg}.{ptf}')
    else: # wildcard
        raise TypeError('Incorrect type of statistical parameter')
    return title, path_OUT


if __name__ == '__main__':
    # ================   User settings (have to be adapted)  ================
    # -- Settings for research domain and parameter:
    #    You can run this script manually for your research domain and parameter or
    #    you can set them in run_ocn_postprocessing.sh script.

    # -- Manual mode (uncomment these lines):
    #start_year = 2003
    #end_year = 2010
    #region = 'Global'
    #param_var = 'burned_area'

    # -- Automatic mode (uncomment these lines)
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])
    region  = sys.argv[3]
    param_var = sys.argv[4]
    print('Actual research domain - fire_xarray:',region)
    print('Actual research parameter - fire_xarray:', param_var)

    # -- Load basic logical settings:
    lsets = logical_settings(
        lcluster = True,        # Are you working on cluster?
        lnc_info = False,       # Do you want to get more information about data?
        station_mode = False,   # Do you want to get values for stations
        lvis_lines = False,      # Do you want to visualize data (line plots)
        lBasemap_moment = True,# Do you want to visualize data on grid for one moment?
    )
    # -- Load other logical parameters:
    lmodis_nat = True          # Use natural PFT or all
    lfire = True                # Is fire_xarray script active?

    # -- Load basic user settings:
    # -- There is not a strict time rule to time axis:
    if lsets.get('lvis_lines'):
        bcc = config.Bulder_config_class(
            ocn = [int(start_year), int(end_year)],
            jul = [int(start_year), int(end_year)],
            orc = [int(start_year), int(end_year)],
            #modis = [int(start_year), int(end_year)],
            #gfed_tot = [int(start_year), int(end_year)],
            #gfed41s = [int(start_year), int(end_year)],
        )
        tlm = bcc.user_settings()
        # -- Get datasets and time perios for them (satellite + ocn):
        av_datasets = get_settigs4_annual_plots(
            lsets.get('lvis_lines'),
            lsets.get('lBasemap_moment'),
            tstart = start_year,
            tstop = end_year,
        )

    # -- Load basic user settings:
    # -- There is a strict time rule to time axis:
    if lsets.get('lBasemap_moment'):
        bcc = config.Bulder_config_class(
            ocn = [int(start_year), int(end_year)],
            jul = [int(start_year), int(end_year)],
            orc = [int(start_year), int(end_year)],
            modis = [int(start_year), int(end_year)],
            gfed_tot = [int(start_year), int(end_year)],
            gfed41s = [int(start_year), int(end_year)],
        )
        tlm = bcc.user_settings()
        # -- Get datasets and time perios for them (satellite + ocn):
        av_datasets = get_settings4maps(
            lsets.get('lvis_lines'),
            lsets.get('lBasemap_moment'),
            tstart = start_year,
            tstop = end_year,
        )
    # -- Get dataset names:
    lst4dsnames = av_datasets.get(param_var)
    # -- Get input paths and NetCDF attributes:
    ipaths, res_param = get_path_in(lst4dsnames, param_var, lsets)
    if lmodis_nat:
        for i in range(len(lst4dsnames)):
            if lst4dsnames[i] == 'BA_MODIS':
                tmp_path, tmp_res_param = get_path_in(
                    [lst4dsnames[i]], 'burned_area_nat', lsets)
                ipaths[i] = tmp_path[0]
                res_param[i] = tmp_res_param[0]

    # -- Get output paths and create folder for results:
    data_OUT = makefolder(get_output_path(lsets).get('fire_xarray') + f'/{param_var}')
    print(f'Your data will be saved at {data_OUT}')

    # -- Load user parameters for datasets (mainly important for plot titles):
    # svname - Short name of the parameter, lvname - Full  name of the parameter,
    # lp_units - Units for 2D plots, cp_units - Units for 3D plots
    svname, lvname, lp_units, cp_units = get_parameters(
        lst4dsnames, param_var, lsets)

    # -- Load extra logical settings for computation (active if lBasemap_moment if True):
    if lsets.get('lBasemap_moment'):
        lcalc = lcalc_settings(
            lstat = True,           # Activate algorithm for mean, std and trends calculations?
            lmean_plot = False,      # Activate algorithm for mean visualization (one figure)?
            lstd_plot = False,       # Activate algorithm for std visualization (one figure)?
            ltrend_plot = False,     # Activate algorithm for trends visualization (one figure)?
            lcollage = True,        # Activate algorithm for collage plots: mean, std, trend
            ldiff_calc = True,      # Activate algorithm for difference calculations?
        )
        # -- Define y axis labal for all figures (plots):
        bm_ylabel = f'{svname}, {cp_units}'
        # -- Get time limits for plot titles and output names:
        frs_yr = get_settings4ds_time_limits(tlm).get(param_var).get('OCN')[0]
        lst_yr = get_settings4ds_time_limits(tlm).get(param_var).get('OCN')[1]

        # -- Get title and output names for maps (MEAN, STD, TREND, COLLAGE):
        m_title, m_path_OUT = plt_title_and_output_name(
            lst4dsnames, data_OUT,
            stat_param = 'MEAN',
            long_name = lvname, short_name = svname, region = region,
            frs_yr = start_year, lst_yr = end_year,
        )
        s_title, s_path_OUT = plt_title_and_output_name(
            lst4dsnames, data_OUT,
            stat_param = 'STD',
            long_name = lvname, short_name = svname, region = region,
            frs_yr = start_year, lst_yr = end_year,
        )
        t_title, t_path_OUT = plt_title_and_output_name(
            lst4dsnames, data_OUT,
            stat_param = 'TREND',
            long_name = lvname, short_name = svname, region = region,
            frs_yr = start_year, lst_yr = end_year,
        )
        c_title, c_path_OUT = plt_title_and_output_name(
            lst4dsnames, data_OUT,
            stat_param = 'COLLAGE',
            long_name = lvname, short_name = svname, region = region,
            frs_yr = start_year, lst_yr = end_year,
        )

        # -- Define datasets for difference metrics (diff = refer - comp_ds):
        if lcalc.get('ldiff_calc'):
            print('Set datsets for calculating difference (diff = refer - comp_ds)')
            get_diff_options = get_settings4diff_data(
                ba_refer = 'BA_MODIS', ba_comp = 'OCN_S2Diag_v4',
                ffire_refer = 'GFED4.1s', ffire_comp = 'OCN_S2Diag_v4')
            refer   = get_diff_options.get(param_var)[0]
            comp_ds = get_diff_options.get(param_var)[1]
            print('Actual refer:', refer, 'Actual comp_ds: ', comp_ds)
            dif_title, dif_path_OUT = plt_title_and_output_name(
                lst4dsnames, data_OUT,
                stat_param = 'DIFF',
                long_name = lvname, short_name = svname, region = region,
                frs_yr = start_year, lst_yr = end_year,
                ds4refer = refer, ds4comp = comp_ds,
            )
            # -- Fast control: Check datasets (refer and comp_ds) in lst4dsnames:
            if ((refer not in lst4dsnames) and (comp_ds not in lst4dsnames)):
                print('There are no datasets (reference or experiment) in lst4dsnames.'
                      ' Please, correct data in user_settings \n')
                sys.exit()


    # =============================    Main program   =======================
    print('START program')
    # -- Get data from NetCDF files:
    lst4data = get_data(ipaths, lst4dsnames, param_var, res_param, tlm)
    # -- Convert data to one grid size (upscalling or interpolation):
    lst4data = get_interpol(lst4data, lst4dsnames, region, param_var, tlm)

    # -- Step 1: Create annual plots for stations and for selected domains:
    # -- Get one point data
    if lsets.get('station_mode') and region == 'Global':
        print(f'One point mode - domain {region} \n')
        points_test = one_point_calc(
            lst4dsnames,
            lst4data,
            param_var,
            lvname,
            svname,
            data_OUT,
            region,
            tlm,
            tstart = start_year,
        )

    # -- Preparing data and creating linear annual plots based on them:
    if lsets.get('lvis_lines'):
        # -- Get user settings for annual plots (title, y label, output name, legend location):
        user_plt_settings = {
            'title' : f'{lvname} over {region} region ',
            'ylabel' : f'{svname}, {lp_units}',
            'output_name' : f'{svname}_{region}.png',
            'legend_pos' : 'upper left',
        }
        # -- Get annual mean data
        amean = annual_mean(lst4data, param_var)
        # -- Create plots:
        one_linear_plot(
            lst4dsnames,
            region,
            param_var,
            amean,
            user_plt_settings,
            data_OUT,
            tlm,
            tstart = start_year,
        )

    # -- Step 2: Create maps based on grid points:
    if lsets.get('lBasemap_moment'):
        # -- Load user class with statistical functions
        stat = Statistic()
        # -- Get actual latitudes and longitudes for each dataset:
        lst4lat = [lst4data[i].lat.values for i in range(len(lst4data))]
        lst4lon = [lst4data[i].lon.values for i in range(len(lst4data))]

        # -- Statistical parameters calculations (MEAN, STD, Time TREND):
        if lcalc.get('lstat'):
            lst4mean = stat.timmean(lst4dsnames, lst4data, param_var, fire_xarray = lfire)
            lst4std  = stat.timstd(lst4dsnames, lst4data, param_var, fire_xarray = lfire)
            lst4trends = stat.timtrend(lst4dsnames, lst4data, param_var, fire_xarray = lfire)
        # -- Visualization of statistical parameters (MAP for each parameter):
        # -- Create 2D  MEAN map:
        if lcalc.get('lmean_plot'):
            one_plot(
                lst4dsnames,
                'mean',
                region, lst4lon, lst4lat,
                lst4mean,
                param_var,
                bm_ylabel, m_title, m_path_OUT,
                tlm,
            )
        # -- Create 2D STD map:
        if lcalc.get('lstd_plot'):
            one_plot(
                lst4dsnames,
                'std',
                region, lst4lon, lst4lat,
                lst4std,
                param_var,
                bm_ylabel, s_title, s_path_OUT,
                tlm,
            )
        # -- Create 2D TREND map:
        if lcalc.get('ltrend_plot'):
            one_plot(
                lst4dsnames,
                'trend',
                region, lst4lon, lst4lat,
                lst4trends,
                param_var,
                bm_ylabel, t_title, t_path_OUT,
                tlm,
            )
        # -- Create collage figure with 2D maps (mean, std, trend):
        if lcalc.get('lcollage'):
            collage_plot(
                # datasets
                lst4dsnames,
                # region, lon, lat
                region, lst4lon, lst4lat,
                # MEAN, STD, TREND stat. data
                lst4mean, lst4std, lst4trends,
                # parameter
                param_var,
                # y label, plot title, output path
                bm_ylabel, c_title, c_path_OUT,
                # user class with settings
                tlm,
                # diff mode = False
                ldiff = False,
            )

        # -- Create collage plot with 2D difference maps (Refer - simulation):
        if lcalc.get('ldiff_calc'):
            # -- Get values for difference (mean, std, trend):
            lst4comp_mean  = stat.get_difference(lst4dsnames, refer, comp_ds, lst4mean)
            lst4comp_std   = stat.get_difference(lst4dsnames, refer, comp_ds, lst4std)
            lst4comp_trend = stat.get_difference(lst4dsnames, refer, comp_ds, lst4trends)
            # -- Get actual latitude and longitude values:
            lst4lon = [lst4comp_mean[i].lon.values for i in range(len(lst4comp_mean))]
            lst4lat = [lst4comp_mean[i].lat.values for i in range(len(lst4comp_mean))]
            # -- Create difference plot:
            collage_plot(
                # datasets
                lst4comp_mean,
                # region, lon, lat
                region, lst4lon, lst4lat,
                # DIFF MEAN, STR, TREND data
                lst4comp_mean, lst4comp_std, lst4comp_trend,
                # parameter
                param_var,
                # y label, title, path out
                bm_ylabel, dif_title, dif_path_OUT,
                # user class
                tlm,
                # diff mode = True
                ldiff = True,
                # reference dataset
                refer = refer,
                # dataset for comparison
                comp_ds = comp_ds,
            )

    print('END program')
# =============================    End of program   =====================
