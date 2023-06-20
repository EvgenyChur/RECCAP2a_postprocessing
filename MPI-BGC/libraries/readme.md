# Scripts description:

This folder has personal modules for work with data in NetCDF and csv formats, SLURM system, PFT functions, line settings and figures.

1. `lib4colors.py` - Module has settings for linear plots (line color and style) depending on: type of *a* - dataset, *b* - PFT, *c* - numbers of plot lines. If you want to add new model simulation or dataset and use it with current visualization functions, you have to add additional dataset plot settings to this module. More detailed information about datasets, colors and ets., you can find in the module description header;

2. `lib4pft.py` - Module has the plunt functional types (PFT) tables with meta information about *OCN* and *ESA-CCI MODIS* PFT (description, numbers, plant type and ets.). If you want to use another PFT, please add metainformation of them into this module;

3. `lib4postprocessing.py` - Module has functions for postprocessing of burned area data based on *OCN simulations* and *ESA-CCI MODISv5.0* dataset:
    - ***ba_postprocessing*** -> allow you to get: **a** - total burned area values by *OCN PFT* and **b** - total natural values of burned area for *ESA-CCI MODIS*. Function results can be used as initial data for furhter postprocessing scripts.

4. `lib4sys_support.py` - Module has functions for work with the file system based on *sys* and *oc* python modules:
    - ***dep_clean*** -> cleaning previous results;
    - ***makefolder*** -> creating new output folder.

5. `lib4upscalling_support.py` - Module has functions for upscalling different grids. At the moment, functions are able to convert *0.25 grid to 0.5 grid*. Other resolutions can be implemented later (by requests):
    - ***get_upscaling_ba_veg_class*** -> upscaling burned area data presented on different PFT from *0.25 grid to 0.5 grid*;
    - ***get_upscaling_ba*** -> upscaling total burned area from *0.25 grid to 0.5 grid*;

6. `lib4visualization.py` - Module has functions for visualization of model results. More information about functions you can find in module comments. Module has:
    - ***line_plots*** -> create *line*, *scatter* or *bar* plots, base on timeseries;
    - ***netcdf_line_plots*** -> create *line* based on DataArray. Used it for NetCDF linear plots;
    - ***plots5_stomata*** -> create *linear plot* for stomatal resistance data with errorbar information;
    - ***tick_rotation_size*** -> auxiliary function with user settings for *tick colors*, *rotation* and *fontsize*;
    - ***line_plot_settings*** -> auxiliary function with user settings for 1D plots;
    - ***hist_settings*** -> auxiliary function with user settings for ***plot_diff_hist***;
    - ***plot_diff_hist*** -> create burned area historgam with a gap between values. (For example: 0-10 and 100-150);
    - ***TaylorDiagram*** -> create Taylor diagram;
    - ***select_domain*** -> auxiliary function with research domain projection properties. Important for 2D plots based on NetCDF data;
    - ***vis_stations*** -> create 2D map with station location on a global map;
    - ***netcdf_grid*** -> create 2D map for one moment of time;
    - ***netcdf_grid_series*** -> create 2D map presented  on different subplots. Collage plot;
    - ***create_fast_xarray_plot*** -> create simple domain map based on xarray options for visualization;
    - ***get_params*** -> auxiliary function for definition of COSMO-CLM output parameter name;
    - ***vis_stat_mode*** -> create linear plot with monthly values based on COSMO-CLM data;
    - ***get_data_m*** -> create linear plot with daily values based on COSMO-CLM data;
    - ***plot_waves*** -> create linear plot for heat and cold waves based on T2m and COSMO-CLM data.

7. `lib4xarray.py` - Module has functions for reading and processing data, and units conversion from different NetCDF files:
    - ***weighted_temporal_mean*** -> calculating yearly average with the corresponding weights of days in each month;
    - ***comp_area_lat_lon*** -> creating mesh grid with cell-area for actual coordinates
    - ***read_ocn*** -> reading NetCDF data with *OCN* model information and converting units to the same units as *JULES* and *ORCHIDEE* models;
    - ***read_jules*** -> reading NetCDF data with *JULES* model information and converting units to the same units as *OCN* and *ORCHIDEE* models;
    - ***read_orchidee*** -> reading NetCDF data with *ORCHIDEE* model information and converting units to the same units as *OCN* and *JULES* models;
    - ***get_data*** -> opening NetCDF data, get initial information about data from file and run algorithms for an initial data preprocessing;
    - ***get_interpol*** -> upscaling or downscaling data to the same grid as OCN;
    - ***annual_mean*** -> calculating annual values for research parameters. Values from this subrotine are used only for linear plots which you can generate from `fire_xarray.py` and `one_linear_plot.py`. Function has an ***additional algorithm for convertation units*** into a special format which is applying for linear plots.

## How to use scripts:
There are two options how to use functions, dictionaries and other variables from these modules:
1. Using current modules into new scripts. If you want to do that, please use code presented below and set an appropriate module name instead of `lib_name`:
```
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries import lib_name
```
Also, you can import only the unic function (dictionary and ets.) from current modules. In that case use:
```
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib_name import param_name
```
where: `lib_name` is module name, `param_name` is function or dictionary. These 2 parameters should be adapted by users.

2. Several modules have *option for debugging* and you can run and test them independently with fast-proceessing data:
    * `lib4upscalling_support.py` -> you have to adapt parameters in ***Users settings*** and run it;
    * `lib4xarray.py` -> you have to adapt parameters in ***Users settings*** and run it.
    ```
    python3 ./lib_name.py
    ```
    where: `lib_name` is module name. Should be adapted by users.

<span style="color:red"><strong><em>Important information:</em></strong></span>
If you want to find place, where the module or function has been applying you can use this command:
```
grep -rn your_string folder
```
where: `your_string` is what you want to find; `folder` is folder where you want to search.
