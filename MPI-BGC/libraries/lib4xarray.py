# -*- coding: utf-8 -*-
"""
Module with functions for reading and processing data from NetCDF files:
    a. weighted_temporal_mean --> Calculating the yearly average with the
                                  corresponding weights of days in each month;
    b. comp_area_lat_lon      --> Creatin mesh grid with cell-area for actual coordinates;
    c. read_ocn               --> Reading NetCDF data with OCN model information and convert
                                  units to the same units as JULES and ORCHIDEE models;
    d. read_jules             --> Reading NetCDF data with JULES model information and convert
                                  units to the same units as OCN and ORCHIDEE models;
    e. read_orchidee          --> Reading NetCDF data with ORCHIDEE model information and
                                  convert units to the same units as OCN and JULES models;
    f. get_data               --> Opening NetCDF data, get initial information
                                  about data from file;
    g. get_interpolation      --> Upscaling or downscaling data to the same grid as OCN
    h. annual_mean            --> Calculation of annual values for research
                                  parameters. Values from this subrotine are used
                                  only for linear plots which you can generate from
                                  fire_xarray.py and one_linear_plot.py. Function
                                  has an ***additional algorithm for convertation
                                  units*** into a special format which is applying
                                  for linear plots.

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de


History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-06-10 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
    1.2    2022-09-15 Evgenii Churiulin, MPI-BGC
           Updated all subrotines
    1.3    2022-10-28 Evgenii Churiulin, MPI-BGC
           Add new function for calculating mean values in accordance with the
           corresponding weights of days in each months. Change script structure
    1.3    2022-11-16 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project.
           Relocated ocn_list with all available simulations to user_settings.
    1.4    2023-03-13 Evgenii Churiulin, MPI-BGC
           get_data unction was updated. 3 new functions for reading OCN, JULES,
           ORCHIDEE data were created.
    1.5    2023-05-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
# -- Standard modules:
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
from typing import Optional
import warnings
warnings.filterwarnings("ignore")

# -- Personal modules:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.user_settings import time_limits, domain_lim, psets
from settings.path_settings import get_path_in
import libraries.lib4upscaling_support as lib4ups
# =============================   Personal functions   ==================

# 2.1 weighted_temporal_mean --> Calculating the yearly average with the
#                                corresponding weights of days in each month.
def weighted_temporal_mean(
        # Input variables:
        ds:xr.DataArray,               # Input data
        var:str,                       # Research variable
        # OUTPUT variables:
        ) -> xr.DataArray:             # The weighted average
    # -- Determine the month length:
    month_length = ds.time.dt.days_in_month
    # -- Calculate the weights:
    wgts = month_length.groupby("time.year") / month_length.groupby("time.year").sum()
    # -- Make sure the weights in each year add up to 1:
    test = (pd.DataFrame(wgts.groupby("time.year")
                             .sum(xr.ALL_DIMS)
                             .values
                         ).apply(lambda x: x.mean())[0]
           )

    if test == 1:
        print('Sum of each year’s weights is equal to 1!')
    else:
        print('Sum of each year’s weights is not equal to 1!')

    # -- Subset our dataset for our variable:
    obs = ds[var]
    # -- Setup our masking for nan values:
    cond = obs.isnull()
    ones = xr.where(cond, 0.0, 1.0)
    # -- Calculate the numerator:
    obs_sum =   (obs * wgts).resample(time = "AS").sum(dim = "time")
    # -- Calculate the denominator:
    ones_out = (ones * wgts).resample(time = "AS").sum(dim = "time")
    # -- Get weighted average:
    average_weighted_temp = obs_sum / ones_out
    # -- Average_weighted_temp = xr.DataArray(average_weighted_temp, name = var):
    average_weighted_temp = average_weighted_temp.to_dataset(name = var)
    return average_weighted_temp

# 2.2 comp_area_lat_lon --> Create mesh grid for actual coordinates
#                           Author: Ana Bastos
def comp_area_lat_lon(
        # Input variables:
        lat:np.array,                 # Latitude values from NetCDF file
        lon:np.array,                 # Longitude values from NetCDF file
        # OUTPUT variables:
    ) -> np.array:                    # area 2D array.
    # Start computations:
    radius = 6.37122e6 # in meters
 
    lat  = np.squeeze(lat); lon = np.squeeze(lon)
    nlat = len(lat)
    nlon = len(lon)
    # -- LATITUDE:
    lat_edge         = np.zeros((nlat + 1))
    lat_edge[0]      = max(-90, lat[0] - 0.5 * (lat[1] - lat[0]));
    lat_edge[1:nlat] = 0.5 * (lat[0:nlat-1] + lat[1:nlat])
    lat_edge[nlat]   = min(90, lat[nlat - 1] - 0.5 * (lat[nlat - 2] - lat[nlat - 1]))
    dlat             = np.diff(lat_edge)
    # -- LONGITUDE:
    lon_edge         = np.zeros((nlon + 1))
    lon_edge[0]      = lon[0] - 0.5 * (lon[1] - lon[0])
    lon_edge[1:nlon] = 0.5 * (lon[0:nlon-1] + lon[1:nlon])
    lon_edge[nlon]   = lon[nlon - 1] - 0.5 * (lon[nlon - 2] - lon[nlon - 1])
    dlon             = np.diff(lon_edge)
    # -- Create mesh with cell size in deg:
    dlon_2d, dlat_2d = np.meshgrid(dlon, dlat)
    lon_2d , lat_2d  = np.meshgrid( lon,  lat)
    dy = radius * (dlat_2d * (np.pi / 180.0))
    dx = radius * np.multiply(dlon_2d * (np.pi / 180.0), np.cos(lat_2d * (np.pi / 180.0)))
    # -- Get cell-area:
    area = np.multiply(dx, dy)
    if np.sum(area) < 0:
        area = -1 * area
    return area

# 2.3 read_ocn --> Read NetCDF data with OCN model information and convert
#                  units to the same units as JULES and ORCHIDEE models
def read_ocn(
        # Input variables:
        path:str,                           # Input path
        ds_name:str,                        # Dataset name
        param:str,                          # Attribute name of the research parameter in current NetCDF
        var:str,                            # Attribute name for the new dataset and futher computations
        # OUTPUT variables:
    ) -> xr.DataArray :                     # Research dataset with correct units
    # -- Local variables
    sec_in_hour = 3600.0      # number of seconds in hour
    hour_in_day = 24.0        # number of hours in day
    g_in_kg     = 1000.0      # gramms in 1 kg
    rec_coef    = 1e-9        # m2 to 1000 km2
    
    # -- Read data
    nc = (
        xr.open_dataset(path, decode_times = False)
          .assign_coords({'time': pd.date_range(psets.get(ds_name)[0],
                                                psets.get(ds_name)[1],
                                         freq = psets.get(ds_name)[2])}))

    # -- Add a new field with area information to current datasets
    nc = nc.assign(xr.Dataset({'area': (('lat', 'lon'),
                      comp_area_lat_lon(nc.lat.values, nc.lon.values))},
                      coords = {'lat' : nc.lat.values, 'lon' : nc.lon.values}))

    # -- convert units to correct format
    if var in ('gpp', 'npp', 'fFire', 'nbp', 'nee'):    
        # Convert kg C m-2 s-1  to gC m-2 yr-1
        nc[param] = (nc[param] * g_in_kg * hour_in_day * sec_in_hour *   
                     nc[param].time.dt.days_in_month)

    elif var == 'burned_area':
        nc['burned_area'] = (nc[param] * nc['area'] * rec_coef * 
                             nc[param].time.dt.days_in_month)    
    #else:  
        # cVeg and LAI parameters should be the same as it was before    
    return nc

# 2.4 read_jules --> Read NetCDF data with JULES model information and convert
#                    units to the same units as OCN and ORCHIDEE models
def read_jules(
        # Input variables:
        path:str,                           # Input path
        ds_name:str,                        # Dataset name
        param:str,                          # Attribute name of the research parameter in current NetCDF
        var:str,                            # Attribute name for the new dataset and futher computations
        # OUTPUT variables:
    ) -> xr.DataArray :                     # Research dataset with correct units
    # -- Local variables
    sec_in_hour = 3600.0      # number of seconds in hour
    hour_in_day = 24.0        # number of hours in day
    g_in_kg     = 1000.0      # gramms in 1 kg
    rec_coef    = 1e-9        # m2 to 1000 km2

    # -- Read data
    nc = xr.open_dataset(path)  

    # -- Rename attributes
    #nc = nc.rename({'longitude':'lon', 'latitude':'lat'})

    # -- Add a new field with area information to current datasets
    nc = nc.assign(xr.Dataset({'area': (('lat', 'lon'),
                      comp_area_lat_lon(nc.lat.values, nc.lon.values))},
                      coords = {'lat' : nc.lat.values, 'lon' : nc.lon.values}))

    # -- convert units to correct format
    if var in ('gpp', 'npp', 'fFire', 'nbp'):
        # Convert kg C m-2 s-1  to gC m-2 yr-1
        nc[param] = (nc[param] * g_in_kg * hour_in_day  * sec_in_hour * 
                     nc[param].time.dt.days_in_month)

    elif var == 'burned_area':
        nc['burned_area'] = ((nc[param] / 100) * nc['area'] * rec_coef) #*
                             #nc[param].time.dt.days_in_month)# * hour_in_day * 
                             #sec_in_hour)
    #else:  jul_nc[jres_param[0]] / 100)* jul_nc['area'] * rec_coef
        # cVeg and LAI parameters should be the same as it was before  
    return nc


# 2.5 read_orchidee --> Read NetCDF data with ORCHIDEE model information and
#                       convert units to the same units as OCN and JULES models
def read_orchidee(
        # Input variables:
        path:str,                           # Input path
        ds_name:str,                        # Dataset name
        param:str,                          # Attribute name of the research parameter in current NetCDF
        var:str,                            # Attribute name for the new dataset and futher computations
        # OUTPUT variables:
    ) -> xr.DataArray :                     # Research dataset with correct units
    # -- Local variables
    nan_values  = 9.96921e+36 # nan values in dataset
    sec_in_hour = 3600.0      # number of seconds in hour
    hour_in_day = 24.0        # number of hours in day
    g_in_kg     = 1000.0      # gramms in 1 kg
    rec_coef    = 1e-9        # m2 to 1000 km2

    # -- Read data
    nc_orh = (
        xr.open_dataset(path, decode_times = False)
          .assign_coords({'time': pd.date_range(psets.get(ds_name)[0],
                                                psets.get(ds_name)[1],
                                         freq = psets.get(ds_name)[2])})
    )

    # -- Rename attributes
    nc_orh = nc_orh.rename({'longitude':'lon', 'latitude':'lat'})

    # -- Add a new field with area information to current datasets
    nc_orh = nc_orh.assign(xr.Dataset({'area': (('lat', 'lon'),
                              comp_area_lat_lon(nc_orh.lat.values,
                                                nc_orh.lon.values))},
                              coords = {'lat' : nc_orh.lat.values,
                                        'lon' : nc_orh.lon.values}))    
    # -- Replace NaN values to NaN
    nc = nc_orh.where(nc_orh[param] != nan_values)

    # -- convert units to correct format
    if var in ('gpp', 'fFire', 'nbp'):
        # Convert kg C m-2 s-1  to gC m-2 yr-1
        nc[param] = (nc[param] * g_in_kg * hour_in_day  * sec_in_hour * 
                     nc[param].time.dt.days_in_month)
  
    elif var == 'burned_area':
        nc['burned_area'] = (nc[param] * nc['area'] * rec_coef *
                              nc[param].time.dt.days_in_month)
    #else:  
        # cVeg and LAI parameters should be the same as it was before
    return nc


# 2.6 get_data -> Open NetCDF data, get initial information about data from file
#                 and run algorithms for an initial data preprocessing
def get_data(
        # Input variables:
        lst4pathin:list[str],                  # Dataset paths
        lst4dsnames:list[str],                 # Dataset names
        var:str,                               # Research parameter
        param_var:list[str],                   # Name of the research parameter into actual dataset
        linfo: Optional[bool] = False,         # Do you want to get information about NetCDF? Default is False
        lresmp: Optional[bool] = True,         # Do you want to get annual values? Default is True
        # OUTPUT variables:
    ) -> list[xr.DataArray]:                   # Preprocessed data for each dataset
    # -- Local variables:
    ocn_id = 'OCN'
    jul_id = 'JUL'
    orc_if = 'ORC'

    # -- Recalculation coefficients:
    rec_coef = 1e-9  # m2 in 1000 km2
    g2kg = 1000      # g in kg
    # -- Preprocessing of netcdf data:
    nc_data = []
    for i in range(len(lst4dsnames)):
        print(lst4dsnames[i])

        # -- Read and convert units of OCN and NDEP data:
        if ((lst4dsnames[i][0:3] == ocn_id) or (lst4dsnames[i] == 'NDEP')):
            ncfile = read_ocn(
                lst4pathin[i], lst4dsnames[i], param_var[i], var
            )
        # -- Read and convert units of JULES data:
        elif lst4dsnames[i][0:3] == jul_id:
            ncfile = read_jules(
                lst4pathin[i], lst4dsnames[i], param_var[i], var
            )
        # -- Read and convert units of ORCHIDEE data:
        elif lst4dsnames[i][0:3] == orc_if:
            ncfile = read_orchidee(
                lst4pathin[i], lst4dsnames[i], param_var[i], var
            )
        else:
            # -- Read satellute datasets and other model experiments
            ncfile = xr.open_dataset(lst4pathin[i])
            # -- Add a new field with area information to current datasets
            ncfile = ncfile.assign(xr.Dataset({'area': (('lat', 'lon'),
                                      comp_area_lat_lon(ncfile.lat.values,
                                                        ncfile.lon.values))},
                                      coords = {'lat' : ncfile.lat.values,
                                                'lon' : ncfile.lon.values}))
            # -- Covert units to correct format:

            # a. Fire datasets: Original data from BA_AVHRR, GFED4.1s are in 
            #    fraction. We have to convert data to burned area. Data from 
            #    BA_MODIS are burned area  
            if var == 'burned_area':
                if lst4dsnames[i] in ('GFED4.1s', 'GFED_TOT', 'GFED_FL'):
                    ncfile['burned_area'] = (ncfile[param_var[i]] * 
                                             ncfile['area'] * rec_coef)
                else:
                    # -- MODIS data has original values 
                    ncfile[param_var[i]] = ncfile[param_var[i]] * rec_coef

            # b. Fire emission datasets:
            elif (var == 'fFire' and lst4dsnames[i] == 'GFED4.1s'):
                ncfile['fFire'] = ncfile[param_var[i]] 

            elif ((var == 'npp' or var == 'gpp') and 
                  (lst4dsnames[i] in ('MOD17A2HGFv061', 'MOD17A3HGFv061'))):
                # Convert kg C m-2 m-1 to gC m-2 yr-1
                ncfile[var] = ncfile[param_var[i]] * g2kg
            #else:
                # You can add more options here

        # -- Convert monthly data to yearly
        if lresmp == True:
            if var in ('lai', 'cVeg') :
                ncfile = ncfile.resample(time = 'A').mean('time')
            else:
                ncfile = ncfile.resample(time = 'A').sum('time')
        # -- Add data to the new list
        nc_data.append(ncfile)
    return nc_data  


# 2.7 get_interpolation --> Get data from NetCDF at the same grid as OCN
def get_interpol(
        # Input variables:
        lst4data:list[xr.DataArray],     # Data from the actual datasets
        lst4dsnames:list[str],           # Names of the research datasets
        domain:str,                      # Research region
        var:str,                         # Research parameter.
        # OUTPUT variables:
    ) -> list[xr.DataArray]:             # Results of reinterpolation
    # -- Local variables:
    ocn_id = 'OCN'
    jul_id = 'JUL'
    orc_id = 'ORC'

    # -- Get simular grids for research domain:
    grid4domain = []
    for i in range(len(lst4dsnames)): 
        print(lst4dsnames[i])
        # -- Select time range for analysis (years for time slice):
        if lst4dsnames[i][0:3] in (ocn_id, jul_id, orc_id):
            ds_name = lst4dsnames[i][0:3]
        else:
            ds_name = lst4dsnames[i]
        # -- Get simular datasets:
        act_ds = lst4data[i].sel(
            # -- Slice by latitudes:
            lat  = slice(domain_lim.get(domain)[0],
                         domain_lim.get(domain)[1]),
            # -- Slice by longitudes:
            lon  = slice(domain_lim.get(domain)[2],
                         domain_lim.get(domain)[3]),
            # -- Time slice
            time = slice(f'{time_limits.get(var).get(ds_name)[0]}', 
                         f'{time_limits.get(var).get(ds_name)[1]}')
        )
        # -- Define grid for interpolation (on this grid will be interpolation)
        if lst4dsnames[i][0:3] == ocn_id:
            inter2grid = act_ds

        if ((lst4dsnames[i] == 'JUL_S2Diag') and (var == 'burned_area')):
            act_ds = act_ds / 13.5
        # -- Add new data to the list:
        grid4domain.append(act_ds) 

    # 2. Interpolation grids v, orc_id
    for i in range(len(lst4dsnames)):
        # -- Select no OCN simulations
        if lst4dsnames[i][0:3] != ocn_id:
            # 2.1: Run upscalling for burned area
            if ((var == 'burned_area') and (lst4dsnames[i][0:3] != orc_id) and
                (lst4dsnames[i][0:3] != jul_id)):

                res360_720 = lib4ups.get_upscaling_ba(grid4domain[i], var, lreport = False)
                grid4domain[i] = res360_720.to_dataset(name = var)

            # 2.2: Run interpolation to OCN grid (all parameters)
            grid4domain[i] = grid4domain[i].interp_like(
                inter2grid.drop_dims('time'), method = 'nearest' )              # interpolation with time ignore

            # 2.3: Add a new field with area information to current datasets
            grid4domain[i] = (
                grid4domain[i].assign(
                    xr.Dataset(
                        {'area': (('lat', 'lon'),
                            comp_area_lat_lon(grid4domain[i].lat.values,
                                              grid4domain[i].lon.values))}, 
                            coords = {'lat' : grid4domain[i].lat.values,
                                      'lon' : grid4domain[i].lon.values}
                    )
                )
            )
    return grid4domain

# 2.8 annual_mean --> Calculation of annual values for research parameters.
#                     Values from this subrotine are used only for linear plots
#                     which you can generate from fire_xarray.py and one_linear_plot.py
def annual_mean(
        # Input variables:
        ds_data:list[xr.Dataset],      # Data from actual research datasets and the relevant names of datasets
        var:str,                       # Research parameter(burned_area, gpp, npp and etc...)
        # OUTPUT variables:
    ) -> list[xr.Dataset]:             # Annual values of the research parameter

    # -- Get year sum or mean values: ds - actual dataset, method: mean or sum
    def agg(ds, method):
        if method == 'sum':
            return ds.sum(dim = {'lat', 'lon'}).groupby('time.year').sum()
        else:
            return ds.sum(dim = {'lat', 'lon'}).groupby('time.year').mean()

    # -- Define convertation coefficients:
    orig    = 1.0   # use original units
    kgc2pgc = 1e-12 # kgC --> PgC     
    gc2pgc  = 1e-15 #  gC --> PgC
    set_rec_coef = {
        'burned_area' : orig  , 'lai' : orig  , 'cVeg' : kgc2pgc, 'npp'   : gc2pgc,
        'gpp'         : gc2pgc, 'nee' : gc2pgc, 'nbp'  : gc2pgc , 'fFire' : gc2pgc,
    }

    rec_coef = set_rec_coef.get(var)

    # 2. Convert units into correct format: In case of: burned area - no changes
    # lai - values by area , cVeg --> from gC m-2 to PgC, other --> from kgC m-2 to PgC
    annual_values = []
    for act_ds in ds_data:
        # -- Define area - values
        if var != 'burned_area':
            area = act_ds['area']
        else:
            area = 1.0  
        param = act_ds[var] * area * rec_coef

        # -- Define final values:
        if   var == 'cVeg':
            annual_values.append(agg(param, 'mean'))
        elif var == 'lai':
            temp = param / area.sum(dim = {'lat', 'lon'})
            annual_values.append(agg(temp, 'mean'))
        else:
            annual_values.append(agg(param, 'sum'))
    return annual_values

if __name__ == '__main__':
    #=============================   User settings   ==========================
    # -- Research dataset (s):
    ds_names = ['OCN_S2Prog_v3', 'ORC_S0']
    #ds_names = ['BA_MODIS', 'OCN_S2.1', 'JULES']
    # -- Research parameters:
    ds_vars  = ['cVeg', 'cVeg']
    #ds_vars  = ['burned_area', 'burnedArea']
    # -- Research var:
    var = 'cVeg'
    #var = 'burned_area'
    # -- Research domain:
    domain   = 'Global'

# =============================    Main program   ===================
    # -- Define input paths (MODIS and OCN):
    dpin, dparam = get_path_in(ds_names, var)
    # -- Read data:
    esa_data = get_data(dpin, ds_names , var, ds_vars)
    # -- Run interpolation:
    esa_ba   = get_interpol(esa_data, ds_names, domain, var)
# =============================    End of program   =================
