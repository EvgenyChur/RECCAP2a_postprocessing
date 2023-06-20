# Scripts description:

The folder `calc` has 3 scripts for solving auxiliary tasks:

1. `one_point.py` - Module for analysis and visualization of data for stations. Module has next functions:
    - ***one_point_calc*** -> function for calculating station parameters. This function creates next output figures for the research parameters:

    *Examples:*

    |    Stations  |     Line plot |  Box plot   |
    |:------------:|:-------------:|:-----------:|
    | ![][fig1a]   | ![][fig1b]    | ![][fig1c]  |

    [fig1a]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/STATIONS.png
    [fig1b]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/burned_area_station_AST1.png
    [fig1c]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/boxplot_burned_area_station_AST1.png

2. `stat_controls.py` - Module for statistical analysis of data presented on model grid. Module has next functions:
    - ***timmean*** -> calculating time mean values;
    - ***timstd*** -> calculating standart devion (STD) values;
    - ***timtrend*** -> calculating time trends;
    - ***get_difference*** -> calculating difference between values (mean, std, trend) or just values.

3. `vis_controls.py` - auxiliary module for data visualization. Module has next functions:
    - ***line_settings*** -> get actual settings for linear plot (linecolors and linestyles);
    - ***one_linear_plot*** -> create linear plot based on the research parameters;
    - ***box_plot*** -> create boxplot for stations;
    - ***one_plot*** -> create plot for mean, std or trend;
    - ***collage_plot*** -> create collage plot for mean, std or trend;
    - ***get_figure4lcc*** -> create collage plot with 2D maps for statistical parameters based on ESA-CCI MODISv5.0 or OCN data (2D maps);
    - ***pft_plot*** -> create total burned area comparison plots for ESA-CCI MODISv5.0 or OCN data devided on different vegetation groups (linear plots).

    *Examples:*

    |  one_linear_plot|   Box_plot |  One_plot   | collage_plot   | get_figure4lcc | pft_plot  |
    |:---------------:|:----------:|:-----------:|:--------------:|:--------------:|:---------:|
    | ![][fig2a]      | ![][fig2b] | ![][fig2c]  | ![][fig2d]     | ![][fig2e]     | ![][fig2f]|

    [fig2a]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/burned_area_station_KAZ.png
    [fig2b]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/boxplot_burned_area_station_KAZ.png
    [fig2c]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/TESTS/FIGURES/FAST_TEST/2D_map4MODIS.png
    [fig2d]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/Collage_BA_Global.png
    [fig2e]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/Global_MEAN4BA_vis.png
    [fig2f]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/VIS_CONTROL/PFT_evgreen.png

## How to set scripts?
1. **one_point.py** --> you don't need to change this module. Nevertheless, if you want to change plot settings you have to change several parameters:
    * `/settings/user_settings.py` -> variables `stations` and `plt_limits_point`. Important `plt_limits_point` depends on your time scale, because of that you can set values in your time range. (current ranges: 1960 - 2023, 1980 - 2023 and 2003 - 2023);
    * Sometimes, there are stations with uniq values. In that case, you can check section **User settings for boxplots and line plots:** implemented into `one_point_calc` function.
    * Function has several local variables. Generally you don't need to change them.

2. **stat_controls.py** --> you don't need to change this module.

3. **vis_controls.py** --> you don't need to change this module.

## How to use scripts?
1. If you want to use these modules you have to add this code into your scripts:
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

2. All these modules have been implemented into the main post-processing software and if you want to run it, use next algorithm:

* You have to open running script **\main\run_ocn_postprocessing.sh** and set your user settings for postprocessing script **\main\fire_xarray.py**;

* Open **\settings\user_settings.py** and set your user settings in:
    - ***start_year*** -> the first year which you want to use in your data;
    - ***logical_settings*** -> general settings for post-processing scripts. You can use these settings (yes, no, yes, yes, no). ;
    - ***calculation_settings*** -> additional settings for post-processing scripts. Additional settings is active only with active `lBasemap_moment` parameter. You can use these basic parameters (yes, yes, yes, yes, no, no, no, yes, yes).  More information about these parameters you can find in the script;
    - ***av_datasets*** -> available datasets. You can add or exclude datasets and model simulations;
    - ***time_limits*** -> use time filter for data. Important - datasets have to have the same time axis, otherwise our statistical data can be incorrect. You can ignore it for the first run; You can ignore it for the first run;
    - ***diff_options*** --> if you want to get differences bettween datasets you have to set this parameter. You can ignore it for the first run;
    - ***stations*** --> you can add or exclude stations;
    - ***plt_limits*** --> settings for plots depending on ***start_year***. You can ignore it for the first run;
    - ***plt_limits_point*** --> you can control your y axis values for station plots based on this parameter. Depending on your start year ***start_year***;

There are a lot of different settings. Nevertheless, postprocessing script can work with basic settings and potentially you can ignore most of these setting variables, for the first time as minimum. More information about these parameters you can find in **\settings\user_settings.py**.

* Open **\settings\path_settings.py** and set your path settings. If you work on MPI-BGC cluster you have to adapt only your output folders from: **\settings\mlocal_set.py** (if you want to use your local computer) or **\settings\mcluster.py** (for cluster);

* Don't forget to save your changes. Run the running script.
```
cd user_path\main\
./run_ocn_postprocessing.sh
```
where: **user_path** -> absolute path

* If everything is fine, program will print you information about output folders!

<span style="color:red"><strong><em>Important information:</em></strong></span>
If you want to find place, where the module or function has been applying you can use this command:
```
grep -rn your_string folder
```
where: `your_string` is what you want to find; `folder` is folder where you want to search.

The `one_point.py` script works only with `Global` domain;
