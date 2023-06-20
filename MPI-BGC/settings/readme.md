# Scripts description:

This folder has important modules, which define work of other scripts for postprocessing. In particularly, scripts have user and path settings and you have to adapt them at the begining of your data processing.

1. `mcluster_set.py` - the module with user path settings applicable for *MPI-BGC* cluster. Potentially, you can use this module without changes.
    - ***datasets_catalog*** -> get actual information about input datasets (OCN, JULES, ORCHIDEE results are no included in it);
    - ***ocn_catalog*** -> get actual input information about *OCN* simulations;
    - ***jules_catalog*** -> get actual input information about *JULES* simulations;
    - ***orchidee_catalog*** -> get actual input information about *ORCHIDEE* simulations;
    - ***dataset_units*** -> get actual auxiliary (shorh and full dataset names, dataset units) information for plots;
    - ***output_folders*** -> get actual output paths for calculation results.

2. `mlocal_set.py` - the mirror module with similar path settings as **\settings\mcluster_set.py**, but applicable for your personal computer. You have to adapt this module for your local computer.

3. `path_settings.py` - this module has functions for reading and transfering correct input, output and auxiliary (shorh and full dataset names, dataset units) information from **\settings\mcluster_set.py** and **\settings\mlocal_set.py** scripts:
    - ***get_path_in*** -> get lists with actual information about input paths and NetCDF attributes of your research datasets or model simulations;
    - ***get_parameters*** -> get auxiliary (shorh and full dataset names, dataset units) information for plots based on the user datasets;
    - ***output_path*** -> get list with actual information about output paths for your postprocessing results.

4. `user_settings.py` - has information about user settings.


## How to use scripts?
There are two options how to use these modules:
1. Using current modules into new scripts. If you want to do that, please use code presented below and set an appropriate module name instead of `lib_name`:
```
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings import lib_name
```
Also, you can import only the unic function (dictionary and ets.) from current modules. In that case use:
```
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib_name import param_name
```
where: `lib_name` is module name, `param_name` is function or dictionary. These 2 parameters should be adapted by users.

I would like to note that module `path_settings` has controlling functions for work with `mcluster_set` or `mlocal_set` and I recommend to import in your scripts only 2 modules: `path_settings` and `user_settings`. Nevertheless, you can import `mcluster_set` and `mlocal_set` directly into your scripts, but you have to understand how to set key words for dictionaries.

2. Modules have *option for debugging* and you can run them independently. I recommend to use this option at the beginning of your work, due to it allows you to understand how these module works:
    * `mcluster_set`, `mlocal_set` and `path_settings` --> check you settings in Section **User settings** and use running commands presented below;
    * `user_settings` --> you can use running commands presented below.

Running commands:
```
cd actual_path/MPI-BGC/settings/
python3 ./script_name.py
```
where `actual_path` is actual data path, `script_name` is script name. These 2 parameters should be adapted by users.

## Important notes:

### Module `user_settings.py`:
Most of the scripts use variables from `user_settings`. Also, module `path_settings` uses information about computer type which is located in the `logical_settings` list of `user_settings` module. If you want to change computer type (*local*, *HPC cluster*) you have to check actual values in ***logical_settings[0]***.

The full list of scripts where `user_settings` module was used see below:
|Index | Script (module):               | Settings:                               |
|:----:|:-------------------------------|:----------------------------------------|
| 1    | /test/ctr_interpolation.py     | logical_settings                        |
| 2    | /test/ctr4ocn_out.py           | logical_settings                        |
| 3    | /test/2dmap4sites.py           | stations                                |
| 4    | /calc/vis_controls.py          | time_limits, plt_limits, clb_limits, layout_settings, clb_diff_limits|
| 5    | /calc/one_point.py             | stations, plt_limits_point              |
| 6    | /settings/path_settings.py     | logical_settings                        |
| 7    | /preprocessing/prep_ESA.py     | logical_settings                        |
| 8    | /preprocessing/prep_LAI.py     | logical_settings, domain_lim            |
| 9    | /libraries/lib4visualization.py| all variables                           |
| 10   | /libraries/lib4upscaling_support.py| logical_settings                    |
| 11   | /libraries/lib4xarray.py       | time_limits, domain_lim, psets          |
| 12   | /main/landcover.py             | time_limits, stations                   |
| 13   | /main/fire_xarray.py           | all variables                           |
| 14   | /main/fire_ratio.py            | time_limits                             |


### Module `path_settings.py`:
Most of the scipts use **/settings/path_settings.py**. The full list of scripts you can find in table:
|Index | Script (module):                    | Settings:                                |
|:----:|:------------------------------------|:-----------------------------------------|
| 1    | /notes/notes4futere.py              | get_path_in                              |
| 2    | /tests/2dmap4sites.py               | output_path                              |
| 3    | /tests/ffire_test.py                | get_path_in, output_path                 |
| 4    | /tests/rund_ts4s0.py                | output_path                              |
| 5    | /tests/OCN_param.py                 | get_path_in, output_path, get_parameters |
| 6    | /tests/lpjFire_coef.py              | output_path                              |
| 7    | /tests/fast_test.py                 | get_path_in, output_path                 |
| 8    | /preprocessing/prep_ESA.py          | get_path_in, output_path                 |
| 9    | /libraries/lib4upscaling_support.py | get_path_in, output_path                 |
| 10   | /libraries/lib4xarray.py            | get_path_in                              |
| 11   | /main/ba_esa_pft.py                 | get_path_in, output_path                 |
| 12   | /main/landcover.py                  | get_path_in, output_path,                |
| 13   | /main/check_ocn_pft.py              | get_path_in, output_path                 |
| 14   | /main/fire_xarray.py                | get_path_in, output_path, get_parameters |
| 15   | /main/ba_ocn_pft.py                 | get_path_in, output_path                 |
| 16   | /main/check_ESA_tbaf.py             | get_path_in, output_path                 |
| 17   | /main/mpost4burn_area.py            | get_path_in, output_path                 |
| 18   | /main/fire_ratio.py                 | get_path_in, output_path                 |

<span style="color:red"><strong><em>Important information:</em></strong></span>
If you want to find place, where the module or function has been applying you can use this command:
```
grep -rn your_string folder
```
where: `your_string` is what you want to find; `folder` is folder where you want to search.
