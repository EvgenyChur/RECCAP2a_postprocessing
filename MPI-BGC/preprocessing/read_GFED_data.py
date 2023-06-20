# -*- coding: utf-8 -*-
"""
Description: Preparing GFED4 data for furher analysis

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    09.02.2023 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
    1.2    2023-06-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================     Import modules     =================
import numpy as np
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
# =============================   Personal functions   =================
def open_GFED(path:str, year:int, groups:str) -> xr.Dataset:
    return xr.open_dataset(f'{path}_{year}.nc', group=groups)

def get_GFED_data(years:np.Array, ds_settings:dict) -> xr.Dataset:
    # -- Local variables:
    pin        = ds_settings.get('pin')
    pout       = ds_settings.get('pout')
    act_group  = ds_settings.get('nc_group')
    sub_group  = ds_settings.get('sub_group')
    old_attrib = ds_settings.get('nc_attrib')
    new_attrib = ds_settings.get('nc_attrib_new')
    # -- Data processing:
    ds_gfed = []
    for yr in years:
        # -- Get information about coordinates from NetCDF:
        nc_meta = open_GFED(pin, yr, act_group)
        # -- Get information about burned area from NetCDF:
        nc_ba   = open_GFED(pin, yr, f'{act_group}/{sub_group}')
        # -- Create new Dataset
        nc_ba[new_attrib] = nc_ba[old_attrib]
        gfed4year = nc_ba[new_attrib]
        gfed4year['lon']  = nc_meta.lon
        gfed4year['lat']  = nc_meta.lat
        gfed4year['time'] = nc_meta.time
        # -- Add current year to common dataset:
        ds_gfed.append(gfed4year)
    # -- Create common datasets with burned area from 2002 - 2020:
    gfed4s = xr.concat(ds_gfed, dim = 'time')
    # -- Save new netcdf:
    gfed4s.to_netcdf(pout)
    return gfed4s

# ================   User settings (have to be adapted)  ================
# -- Main path for data:
mpath = '../people/evchur/GFED_2002-2020'                                       # This path was changed because of security reasons
# -- Time limits
trange = np.arange(2002, 2021, 1)
# -- Research parameters:
params = ['BA_TOT', 'BA_FL', 'C_AG_TOT', 'C_BG_TOT', 'C_AG_FL', 'C_BG_FL']
# -- Settings for parameters from NetCDF file:
set4data = {
    # Total fire burned area:
    'BA_TOT' : {
        'pin'           : mpath + '/Model500m_2002-2020yr_025d',                # Input path (data with burned area)
        'pout'          : mpath + '/GFED_burned_area_2002-2020_025d.nc',        # Ouput path
        'nc_group'      : 'MOD_CMG025',                                         # Main NetCDF group
        'sub_group'     : 'burned_area',                                        # Subgroup from NetCDF file
        'nc_attrib'     : 'BA_TOT',                                             # Attribute from subgroup
        'nc_attrib_new' : 'burned_area',                                        # New attribute name
    },
    # Fire-related forest burned area:
    'BA_FL' : {
        'pin'           : mpath + '/Model500m_2002-2020yr_025d',
        'pout'          : mpath + '/GFED_FL_burned_area_2002-2020_025d.nc',
        'nc_group'      : 'MOD_CMG025',
        'sub_group'     : 'burned_area',
        'nc_attrib'     : 'BA_FL',
        'nc_attrib_new' : 'burned_area',
    },
    # Total biomass burning carbon emissions from aboveground:
    'C_AG_TOT' : {
        'pin'           : mpath + '/Model500m_2002-2020yr_025d',
        'pout'          : mpath + '/GFED_C_AG_TOT_2002-2020_025d.nc',
        'nc_group'      : 'MOD_CMG025',
        'sub_group'     : 'emissions',
        'nc_attrib'     : 'C_AG_TOT',
        'nc_attrib_new' : 'c_ag_tot',
    },
    # Total biomass burning carbon emissions from belowground:
    'C_BG_TOT' : {
        'pin'           : mpath + '/Model500m_2002-2020yr_025d',
        'pout'          : mpath + '/GFED_C_BG_TOT_2002-2020_025d.nc',
        'nc_group'      : 'MOD_CMG025',
        'sub_group'     : 'emissions',
        'nc_attrib'     : 'C_BG_TOT',
        'nc_attrib_new' : 'c_bg_tot',
    },
    # Fire-related forest loss carbon emissions from aboveground:
    'C_AG_FL' : {
        'pin'           : mpath + '/Model500m_2002-2020yr_025d',
        'pout'          : mpath + '/GFED_C_AG_FL_2002-2020_025d.nc',
        'nc_group'      : 'MOD_CMG025',
        'sub_group'     : 'emissions',
        'nc_attrib'     : 'C_AG_FL',
        'nc_attrib_new' : 'c_ag_fl',
    },
    # Fire-related forest loss carbon emissions from belowground:
    'C_BG_FL' : {
        'pin'           : mpath + '/Model500m_2002-2020yr_025d',
        'pout'          : mpath + '/GFED_C_BG_FL_2002-2020_025d.nc',
        'nc_group'      : 'MOD_CMG025',
        'sub_group'     : 'emissions',
        'nc_attrib'     : 'C_BG_FL',
        'nc_attrib_new' : 'c_bg_fl',
    },
}

# =============================    Main program   =======================
if __name__ == '__main__':
    ds = []
    for var in params:
        print(f'Data processing for {var}')
        ds.append(get_GFED_data(trange, set4data.get(var)))
        print(f'Data for {var} were preprossed', '/n')
# =============================    End of program   ===================
