# -*- coding: utf-8 -*-
"""
Task : Create linear plot for actual parameter

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-08-08 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project 
    1.3    2023-02-13 Evgenii Churiulin, MPI-BGC
           Variable res_param was changed due to changes into path_settings module
    1.4    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
# 1.1  Standard modules
import os
import sys
import xarray as xr
# 1.2 Personal modules
sys.path.append(os.path.join(os.getcwd(),'..'))
from settings.path_settings import get_parameters, get_path_in, output_path
from libraries.lib4sys_support import makefolder
from calc.vis_controls import one_linear_plot
from libraries import lib4xarray as xrlib
# =============================   User settings   =====================

# Use MODIS natural PFT or all (yes - True, no - False)
lmodis_nat = True

# Research region ('Global', 'Europe', 'Tropics', 'NH')
region  = 'Global'
# Research parameter
param_var = 'burned_area'
# Research datasets (OCN simulations + other datasets):
#lst4dsnames =  ['OCN_S2.1', 'OCN_S3.1', 'OCN_S2.1_nf', 'OCN_S3.1_nf' ]
#lst4dsnames =  ['OCN_S2Prog', 'OCN_S2Diag', 'JULES']
lst4dsnames = ['OCN_S2Prog', 'OCN_S2Diag']

# -- Get output path and create output folder for results:
pout   = makefolder(output_path().get('OCN_param')) 
print(f'Your data will be saved at {pout}')

# -- Settings for plot:
# Get plot lables info from NetCDF 
svname, lvname, lp_units, cp_units = get_parameters(lst4dsnames, param_var)
user_plt_settings = {
    'title'       : f'{lvname} over {region} region ',
    'ylabel'      : f'{svname}, {lp_units}',
    'output_name' : f'{svname}_{region}.png',
    'legend_pos'  : 'upper left',
}
# -- Time limits for JULES. OCN time limits you can set in /settings/user_settings.py
year_start = '2003'
year_stop = '2020'
# =============================    Main program   =======================
if __name__ == '__main__':
    print('START program')
    # -- Get input paths and actual NetCDF reserch attributes:
    ipaths, res_param = get_path_in(lst4dsnames, param_var)
    if lmodis_nat == True:
        for i in range(len(lst4dsnames)):
            if lst4dsnames[i] == 'BA_MODIS':
                tmp_ipath, tmp_res_param = get_path_in(
                    ['BA_MODIS'], 'burned_area_nat')
                ipaths[i]    = tmp_ipath[0]
                res_param[i] = tmp_res_param[0]
    # -- Get data:
    lst4data = xrlib.get_data(ipaths, lst4dsnames, param_var, res_param)
    # Convert data to one grid size
    lst4data = xrlib.get_interpol(lst4data, lst4dsnames, region, param_var)
    # Get annual mean values
    amean    = xrlib.annual_mean(lst4data, param_var)
    # -- Get JULES metainformation (path, labels and ets.)
    jds = ['JUL_S2Prog']
    jipaths, jres_param = get_path_in(jds, param_var)
    jsvname, jlvname, jlp_units, jcp_units = get_parameters(jds, param_var)
    print(jipaths[0], jres_param[0])
    # Get JULES data
    jul_nc = xr.open_dataset(jipaths[0])
    # -- Rename attributes:
    #jul_nc = jul_nc.rename({'longitude':'lon', 'latitude':'lat'})
    jul_nc = jul_nc.assign(xr.Dataset({'area': (('lat', 'lon'),
                             xrlib.comp_area_lat_lon(jul_nc.lat.values,
                                                     jul_nc.lon.values))},
                                   coords = {'lat' : jul_nc.lat.values,
                                             'lon' : jul_nc.lon.values}))
    rec_coef = 1e-9
    #jul_nc['burned_area'] = (
    #    jul_nc[jres_param[0]] * jul_nc['area'] * rec_coef *
    #    jul_nc[jres_param[0]].time.dt.days_in_month * 24 * 3600
    #)

    jul_nc['burned_area'] = ((
        jul_nc[jres_param[0]] / 100)* jul_nc['area'] * rec_coef #*
        #jul_nc[jres_param[0]].time.dt.days_in_month #* 24 * 3600
    )

    jul_ba = (jul_nc['burned_area'].sum(dim = {'lat', 'lon'})
                                   .sel(time = slice(year_start,year_stop))
                                   .groupby('time.year').sum()
    )
    lst4dsnames = lst4dsnames + ['JUL_S2Prog']
    amean.extend([jul_ba])
    # Create linear plot
    one_linear_plot(lst4dsnames, region , param_var, amean, user_plt_settings, pout)
    print('END program')
#=============================    End of program   ============================
