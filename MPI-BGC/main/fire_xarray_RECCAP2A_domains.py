# -*- coding: utf-8 -*-
"""
Script for reading NetCDF files with information about fire or burned area by RECCAP2 domain


Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de


History:
Version    Date       Name
---------- ---------- ----
    1.1    2023-10-30 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2023-11-13 Evgenii Churiulin, MPI-BGC
           Code refactoring + add package import

"""
# =============================     Import modules     ==================
import os
import sys
import warnings
import xarray as xr
import pandas as pd
warnings.filterwarnings("ignore")
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings import (logical_settings, config, get_path_in, get_output_path,
    get_parameters, get_settigs4_annual_plots, get_settings4reccap2_domains,
    get_settings4plots)
from libraries import get_data, get_interpol, annual_mean, makefolder
from calc import one_linear_plot, seaborn_char_plot
# =============================   Personal functions   ==================

if __name__ == '__main__':
    # ================   User settings (have to be adapted)  ================
    # -- Settings for research domain and parameter:
    #    You can run this script manually for your research domain and parameter or
    #    you can set them in run_ocn_postprocessing_reccap.sh script.

    # -- Manual mode (uncomment these lines):
    #start_year = 1960    # First moment of time
    #end_year = 2024      # Last year
    #region    = 'Global' # Research domain
    #param_var = 'lai'    # Research parameter
    # -- Automatic mode (uncomment these lines)
    start_year = sys.argv[1]
    end_year = sys.argv[2]
    region     = sys.argv[3]
    param_var  = sys.argv[4]
    print('Actual research domain - fire_xarray:', region)
    print('Actual research parameter - fire_xarray:', param_var)

    # -- Load basic logical settings:
    lsets = logical_settings(lcluster = True, lvis_lines = True)
    # -- Load other logical parameters:
    lnc_info = lsets.get('lnc_info')    # Do you want to get more information about data?
    lmodis_nat = True                   # Use natural PFT or all

    # -- Load basic user settings:
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
    lst4dsnames = av_datasets.get(param_var)

    # -- Get input paths and NetCDF attributes:
    ipaths, res_param = get_path_in(lst4dsnames, param_var, lsets)
    if lmodis_nat:
        for i in range(len(lst4dsnames)):
            if lst4dsnames[i] == 'BA_MODIS':
                tmp_path, tmp_res_param = get_path_in([lst4dsnames[i]], 'burned_area_nat', lsets)
                ipaths[i] = tmp_path[0]
                res_param[i] = tmp_res_param[0]

    # -- Get output paths and create folder for results:
    data_OUT = get_output_path(lsets).get('fire_xarray')
    data_OUT = makefolder(data_OUT + f'/{param_var}')
    print(f'Your data will be saved at {data_OUT}')

    # -- Get initial parameters for research datasets:
    #   1. svname    - Short name of the parameter
    #   2. lvname    - Full  name of the parameter
    #   3. lp_units  - Units for 2D plots
    #   4. cp_units  - Units for 3D plots
    svname, lvname, lp_units, cp_units = get_parameters(
        lst4dsnames, param_var, lsets)

    # -- RECCAP2A research domains:
    reccap_zone = [
        'USA', 'Canada', 'Central_America', 'Northern_South_America', 'Brazil',
        'Southwest_South_America', 'Europe', 'Northern_Africa', 'Equatorial_Africa',
        'Southern_Africa','Russia', 'Central_Asia', 'Mideast', 'China', 'Korea_and_Japan',
        'South_Asia', 'Southeast_Asia', 'Oceania',
    ]
    #reccap_zone = ['USA']
    # -- Get RECCAP2 axis limits
    set4plot = get_settings4reccap2_domains(tlm)

    # =============================    Main program   =======================
    print('START program')
    if region == 'Global':
        # -- Get initial data from NetCDF:
        lst4data = get_data(
            ipaths,
            lst4dsnames,
            param_var,
            res_param,
            tlm,
        )
        # -- Convert data to one grid size (upscalling or interpolation):
        lst4data = get_interpol(
            lst4data,
            lst4dsnames,
            region,
            param_var,
            tlm,
        )
        # -- Open dataset with domain mask:
        for zone in reccap_zone:
            # PATH WAS CORRECTED -> !!!!!!!!!!
            ds_mask = xr.open_dataset(
                f'../{zone}_domain.nc')
            lst4data_domain = []
            for i in range(len(lst4data)):
                lst4data[i]['mask'] = ds_mask['mask']
                lst4data_domain.append(lst4data[i].where(lst4data[i]['mask'] == 1))
            # -- Get plot settings (title, y_axis_label, output path, legend location):
            user_plt_settings = {
                'title'       : f'{lvname} over {zone} RECCAP2 domain ',
                'ylabel'      : f'{svname}, {lp_units}',
                'output_name' : f'{svname}_{zone}.png',
                'legend_pos'  : 'upper left',
            }
            user_plt_settings_snb = {
                'title'       : f'{lvname} over {zone} RECCAP2 domain ',
                'ylabel'      : f'{svname}, {lp_units}',
                'output_name' : f'{svname}_{zone}_seaborn.png',
                'legend_pos'  : 'upper left',
            }
            # -- Get annual mean data:
            print('Annual sum / mean values: \n')
            amean = annual_mean(lst4data_domain, param_var)
            # -- Create linear plot:
            one_linear_plot(
                lst4dsnames,
                region,
                param_var,
                amean,
                user_plt_settings,
                data_OUT,
                tlm,
                ymin  = set4plot.get(param_var).get(zone)[0],
                ymax  = set4plot.get(param_var).get(zone)[1],
                ystep = set4plot.get(param_var).get(zone)[2],
                rmode = 'RECCAP2',
            )
            # -- Prepare data for seaborn diagram:
            lst_test_amean = []
            for i in range(len(amean)):
                lst_test_amean.append(
                    pd.concat(
                        [
                            pd.Series(amean[i].values, index = amean[i].year),
                            pd.Series(lst4dsnames[i], index = amean[i].year),
                        ], axis = 1
                    )
                )
            df_zone = pd.concat(lst_test_amean, axis = 0)
            df_zone.columns = ['data', 'sim']
            # PATH WAS CORRECTED ->!!!!!!!!
            df_zone.to_csv(f'../df_{zone}.csv')
            # -- Create a seaborn diagram:
            seaborn_char_plot(
                lst4dsnames,
                df_zone,
                data_OUT,
                user_plt_settings_snb,
                tlm,
                ymin  = set4plot.get(param_var).get(zone)[0],
                ymax  = set4plot.get(param_var).get(zone)[1],
                ystep = set4plot.get(param_var).get(zone)[2],
            )
    print('END program')
# =============================    End of program   =====================
