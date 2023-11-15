# -*- coding: utf-8 -*-
"""
Description: Create land/sea masks for RECCAP2 research domains:

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    05.11.2023 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
"""

#=============================     Import modules     ==========================
import os
import sys
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import numpy as np


class Reccap2a_domains:
    """Create RECCAP2 research domains:"""
    def __init__(self):
        self.var_name = 'MASK'
        self.isvalue = 1
        self.nonvalue = 0
        self.ocn_lat_start = 90.0
        self.ocn_lat_end = -60.0
        self.domains_RECCAP2 = {
            'USA'                     :  0,
            'Canada'                  :  1,
            'Central_America'         :  2,
            'Northern_South_America'  :  3,
            'Brazil'                  :  4,
            'Southwest_South_America' :  5,
            'Europe'                  :  6,
            'Northern_Africa'         :  7,
            'Equatorial_Africa'       :  8,
            'Southern_Africa'         :  9,
            'Russia'                  : 10,
            'Central_Asia'            : 11,
            'Mideast'                 : 12,
            'China'                   : 13,
            'Korea_and_Japan'         : 14,
            'South_Asia'              : 15,
            'Southeast_Asia'          : 16,
            'Oceania'                 : 17,
        }

    # -- Select mask for RECCAP2 domains:
    def select_domain(self, pin:int, region:str):
        """Get RECCAP2 domain mask"""
        try:
            ds = xr.open_dataset(pin)
        except:
            print("There is no input dataset")

        ds_mask = (
            ds[self.var_name][self.domains_RECCAP2.get(region)]
                .sel(
                    lat = slice(
                        self.ocn_lat_start,
                        self.ocn_lat_end,
                    )
                )
                .where(
                    ds[self.var_name][self.domains_RECCAP2.get(region)] == self.isvalue
                )
            .data
        )
        # -- Close dataset
        ds.close()
        return ds_mask


    def save_domain(
        self, region:str, domain_mask:np.array, lat:np.array, lon:np.array, pout:str):
        """Save new domain on OCN grid:"""
        ds = xr.DataArray(
            data = domain_mask,
            dims = ['lat', 'lon'],
            coords = dict(
                lat = lat,
                lon = lon,
            ),
            attrs = {
                'title' : f'RECCAP2A research domain: {self.domains_RECCAP2.get(region)}',
                'autors' : 'Evgenii Churiulin, Ana Bastos'
            }
        )
        # -- Settings for tot_ba_fraction:
        ds.name = 'mask'
        ds.attrs['long_name'] = 'Reccap2A domain mask'
        ds.attrs['units'] = '0-1, unitless'
        # -- Save NetCDF file:
        ds.to_netcdf(pout)


if __name__ == '__main__':
    # ============================= Users settings =========================
    # -- RECCAP2A research domains:
    reccap_zone = [
        'USA', 'Canada', 'Central_America', 'Northern_South_America', 'Brazil',
        'Southwest_South_America', 'Europe', 'Northern_Africa', 'Equatorial_Africa',
        'Southern_Africa','Russia', 'Central_Asia', 'Mideast', 'China', 'Korea_and_Japan',
        'South_Asia', 'Southeast_Asia', 'Oceania',
    ]

    # -- Input data:
    main = '../scratch/evchur/RECCAP2_DOMAINS'
    pin  = f'{main}/GCP_18regions_mask_0.5deg_corr.nc'

    # -- Coordinates of OCN grid
    lat1, lat2 = 89.75, -60.25
    lon1, lon2 = -179.75, 180.25
    step_lat, step_lon = -0.5, 0.5

    # =============================    Main program   ======================
    # -- Step 1. Reverse by CDO latitudes from S-N to N-S:
    #cdo invertlat file_in file_out

    # -- Step 2 Data processing:
    reccap_filter = Reccap2a_domains()
    # -- Get RECCAP2 domains and save them into new dataarrays:
    for zone in reccap_zone:
        reccap_filter.save_domain(
            zone,
            reccap_filter.select_domain(pin, zone), 
            np.arange(lat1, lat2, step_lat),
            np.arange(lon1, lon2, step_lon),
            f'{main}/{zone}_domain.nc')
