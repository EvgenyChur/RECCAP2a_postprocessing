# -*- coding: utf-8 -*-
"""
Task: Realization of statistical algorithms for evaluation of OCN results

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-07-7 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.3    2023-05-04 Evgenii Churiulin, MPI-BGC
           Small changes related to code refactoring
    1.4    2023-11-10 Evgenii Churiulin, MPI-BGC
           Prepared for package and created common class Statistic
"""
# =============================     Import modules     ====================
import numpy as np
import xarray as xr
from typing import Optional
import warnings
warnings.filterwarnings("ignore")
# =============================   Personal functions   ====================

class Statistic:
    """Statistical parameters for research datasets (grid points):"""
    def __init__(self):
        pass

    def timmean(
            self, lst4dts:list[str], lst4data:list[xr.DataArray], var:str, **kwargs
        ) -> list[xr.Dataset]:
        """ Get actual data for MEAN calculations (for each grid point):

        **Input variables:**

            lst4dts - Names of datasets
            lst4data - Research datasets at the same order as **lst4dts**
            var - Research parameter.
            **kwargs - Other parameters ('fire_xarray' or 'fire_ratio' with True/False values)

        **Output variables:**
            lst4mean - Mean values for the research datasets.
        """
        return [
            lst4data[i][var].mean(['time']) if kwargs.get('fire_xarray') == True else
            lst4data[i].mean(['time'])
            for i in range(len(lst4dts))
        ]


    def timstd(
            self, lst4dts:list[str], lst4data:list[xr.DataArray],var:str, **kwargs
        ) -> list[xr.Dataset]:
        """ Get actual data for STD calculations (for each grid point):

        **Input variables:**

            lst4dts - Names of datasets
            lst4data - Research datasets at the same order as **lst4dts**
            var - Research parameter.
            **kwargs - Other parameters ('fire_xarray' or 'fire_ratio' with True/False values)

        **Output variables:**
            lst4mean - Mean values for the research datasets.
        """
        return [
            lst4data[i][var].std(['time']) if kwargs.get('fire_xarray') == True else
            lst4data[i].std(['time'])
            for i in range(len(lst4dts))
        ]


    def timtrend(
            self, lst4dts:list[str], data_list:list[xr.DataArray], var:str, **kwargs
        ) -> list[xr.Dataset]:
        """ Trend values for research datasets (for each grid point)

        **Input variables:**

            lst4dts - Names of datasets
            data_list - Research datasets at the same order as **lst4dts**
            var - Research parameter.
            **kwargs - Other parameters ('fire_xarray' or 'fire_ratio' with True/False values)

        **Output variables:**
            lst4mean - Mean values for the research datasets.
        """

        # Start computations:
        # -- Get actual data for TIME TRENDS calculations
        lst4data  = []  # list for data
        lst4years = []  # list for years

        for i in range(len(lst4dts)):
            if kwargs.get('fire_xarray'):
                lst4data.append(data_list[i][var].values)
            elif kwargs.get('fire_ratio'):
                lst4data.append(data_list[i].values)
            lst4years.append(data_list[i].time.dt.year.values )
           # lst4years.append(data_list[i].year.values )

        # -- Get actual time trends
        lst4trends = []
        for i in range(len(lst4dts)):

            # Datasets have NaN values for water objects. Such points shoud be
            # changed to zero
            lst4data[i][np.isnan(lst4data[i])] = 0

            # Reshape to an array with as many rows as years and as
            # many columns as there are pixels
            val = lst4data[i].reshape(len(lst4years[i]), -1)
            # Do a first-degree polyfit
            regressions = np.polyfit(lst4years[i], val, 1)
            # Get the coefficients back
            trends = regressions[0,:].reshape(lst4data[i].shape[1],
                                              lst4data[i].shape[2])

            lon = data_list[i].lon.values
            lat = data_list[i].lat.values

            trends = xr.DataArray(trends,
                                  coords = dict(lat =  lat, lon =  lon),
                                  name = 'trends')
            lst4trends.append(trends)
        return lst4trends


    def get_difference(
            self, dtset_list:list[str], refer_ds:str, comp_ds:str, dt_list:list[xr.DataArray],
        ) -> list[xr.DataArray]:
        """ Get values for comparsion differences between differentdatasets.
        (for example: diff = ESA MODIS - OCN)

        **Input variables:**

            dtset_list - List of datasets
            refer_ds - Reference dataset (for example: MODIS)
            comp_ds - Research dataset (for example: OCN)
            dt_list - Data list for comparison (for example: mean, std, trend lists)

        **Output variables:**
            lst4param - List of parameters in comp_ds grid (reference_ds, comparison_ds, diff).
        """
        # Start computations:
        lst4param  = []
        # Define reference and research datasets (simulations)
        for i in range(len(dtset_list)):
            if dtset_list[i] == refer_ds:
                ref_data = dt_list[i]
            elif dtset_list[i] == comp_ds:
                comp_var = dt_list[i]
        # Get difference
        diff = ref_data - comp_var
        # Create lists
        lst4param.extend([ref_data, comp_var, diff])
        return lst4param
