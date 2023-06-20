# Scripts description:

This folder has personal scripts for postprocessing model and satellite data:

1. `ba_esa_pft.py` - script for calculating statistical parameters (MEAN, STD, TIME TREND) based on *ESA-CCI MODISv5.0* data and visualizing them as collage plots. Script has several subfunctions:
    - ***get_title_path*** -> get actual plot subtitle for each ESA-CCI PFT;
    - ***get_mean_std*** -> get annual MEAN and STD values for each grid points;
    - ***get_trend*** -> get annual time trend for each grid points.

    *Examples:*

    |    MEAN      |      STD      |  TIME TREND |
    |:------------:|:-------------:|:-----------:|
    | ![][fig1a]   | ![][fig1b]    | ![][fig1c]  |

    [fig1a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/ESA_PFT/Global_MEAN4BA_vis.png
    [fig1b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/ESA_PFT/Global_STD4BA_vis.png
    [fig1c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/ESA_PFT/Global_TREND4BA_vis.png

2. `ba_esa_ocn.py` - script for calculating statistical parameters (MEAN, STD, TIME TREND) based on *OCN* data and visualizing them as collage plots.

    *Examples:*

    |    MEAN      |     STD       |  TIME TREND |
    |:------------:|:-------------:|:-----------:|
    | ![][fig2a]   | ![][fig2b]    | ![][fig2c]  |

    [fig2a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/OCN_PFT/Global_MEAN4BA_vis.png
    [fig2b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/OCN_PFT/Global_STD4BA_vis.png
    [fig2c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/OCN_PFT/Global_TREND4BA_vis.png

3. `check_ESA_tbaf.py` - script for calculating differences between natural total annual burned area fraction (tbaf) calculated based on *ESA-CCI MODIS* data and total annual land cover fraction (tland) calculated based on *OCN* natural PFT. Script has several subfunctions:
    - ***get_data*** -> the local function for reading NetCDF data;

    *Examples:*

    | All PFT OCN  | Natura PFT OCN |  DIFF (All - NAT) | Monthly DIFF | Annual DIFF (BA - VEG)  | Bad points (BA > VEG) |
    |:------------:|:--------------:|:-----------------:|:------------:|:-----------------------:|:---------------------:|
    | ![][fig3a]   | ![][fig3b]     | ![][fig3c]        | ![][fig3d]   | ![][fig3e]              | ![][fig3f]            |

    [fig3a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_TBAF/lfrac_all_PFT.png
    [fig3b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_TBAF/lfrac_nat_PFT.png
    [fig3c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_TBAF/lfrac_diff.png
    [fig3d]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_TBAF/monthly_fdiff_2011.png
    [fig3e]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_TBAF/annual_fdiff_2011.png
    [fig3f]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_TBAF/bad_points.png

4. `check_ocn_pft.py` - create burned area comparison plots for *OCN* and *ESA-CCI MODIS* PFT devided on different groups based on vegetation types. Script has several subfunctions:
    - ***read_data*** -> Reading burned area actual datasets (model simulations) and converting them into OCN grid (720x300);
    - ***calc_group*** -> calculating total burned area data for corresponding vegetation groups.

    *Examples:*

    | CROPS        | GRASS          |   EVGREEN TREE    | DECID TREE   |
    |:------------:|:--------------:|:-----------------:|:------------:|
    | ![][fig4a]   | ![][fig4b]     | ![][fig4c]        | ![][fig4d]   |

    [fig4a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/PFT_COMP/PFT_crops.png
    [fig4b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/PFT_COMP/PFT_grass.png
    [fig4c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/PFT_COMP/PFT_evgreen.png
    [fig4d]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/PFT_COMP/PFT_decid.png

5. `fire_ratio.py` - script for creating a collage with the carbon ration (fFire / burned Area);

    | BA coef    | fFire coef | Carbon ratio  |
    |:----------:|:----------:|:-------------:|
    | ![][fig5a] | ![][fig5b] | ![][fig5c]    |

    [fig5a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/FIRE_RATIO/ba_coef_Europe.png
    [fig5b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/FIRE_RATIO/ffire_coef_Europe.png
    [fig5c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/FIRE_RATIO/carbon_ration_Europe.png

6. `fire_xarray.py` - main script for postprocessing of models (OCN, JULES, ORCHIDEE) and satellite information.

    *Examples: Burned Area*

    | Global        | Station        | Global maps  | Global maps (diff)   |
    |:-------------:|:--------------:|:------------:|:--------------------:|
    | ![][fig6a]    | ![][fig6b]     | ![][fig6c]   | ![][fig6d]           |

    [fig6a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/FIRE_XARRAY/BA_Global.png
    [fig6b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/FIRE_XARRAY/boxplot_burned_area_station_KAZ.png
    [fig6c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/FIRE_XARRAY/Collage_BA_Global.png
    [fig6d]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/FIRE_XARRAY/Diff_BA_BA_MODIS_OCN_S2Diag_v3_Global.png

7. `landcover.py` - script for processing of landcover fraction by PFT:
    1. Calculating and visualisation of burned area difference (GFED - OCN) by PFT
    2. Calculating and visualisation of PFT fraction for random points (stations)

    *Examples:*

    | PFT in S2Prog | PFT in S2Diag  | BA DIFF by PFT (ESA-CCI - S2Diag) | BA DIFF by PFT (ESA-CCI - S2Prog)   |
    |:-------------:|:--------------:|:---------------------------------:|:-----------------------------------:|
    | ![][fig7a]    | ![][fig7b]     | ![][fig7c]                        | ![][fig7d]                          |

    [fig7a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_BA_by_PFT/PFT_in_OCN_S2Prog.png
    [fig7b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_BA_by_PFT/PFT_in_OCN_S2Prog.png
    [fig7c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_BA_by_PFT/BA_DIFF_OCN_S2Prog_BA_MODIS.png
    [fig7d]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/MAIN/DIFF_BA_by_PFT/BA_DIFF_OCN_S2Diag_BA_MODIS.png

8. `mpost4burn_area.py` - script for post-processing of *OCN* and *ESA-CCI MODISv5.0*. In case of OCN model, script uses model output *OCN_{name}_firepft.nc* created based on modernized script ***[create_trendy_output_fire.sh][1]*** and calculate total burned area values over all natural PFT. Otherwise, script uses original *ESA-CCI MODISv5.0*, select natural PFT, and calculate total values. You have to use this script before `fire_xarray.py` or `run_ocn_postprocessing.sh`.

9. `run_ocn_postprocessing.sh` -> shell script for running main script for data processing **/main/fire_xarray.py**


## How to set and use scripts:
### Scripts `ba_esa_pft.py` and `ba_esa_ocn.py`:
1. Open scripts and set your personal settings in section **User Settings**;
2. These scripts use several personal modules. Nevetheless, you should not change them and you have to adapt only **/settings/mcluster.py** or **/settings/mlocal.py** and use correct values in **logical_settings[0]** parameter from ***/settings/user_settings***.
3. Run scripts `python3 ./ba_esa_pft.py` or `python3 ./ba_ocn_pft.py` and check your results in output folders.

The full list of personal modules which are presented in script:
- ***/libraries/lib4pft*** -> module with metainformation about PFTs (OCN, ESA-CCI MODISv5.0);
- ***/libraries/lib4sys_support*** -> module for work with file system;
- ***/libraries/lib4xarray*** -> module for data processing;
- ***/calc/lib4vis_control*** -> module for controlling work of **/libraries/lib4visualization.py**;
- ***/settings/path_settings*** -> module for controlling work of **/settings/mcluster.py** or **/settings/mlocal.py**;
- ***/settings/user_settings*** -> modules with global user settings.

### Script `check_ESA_tbaf.py`

Script uses functions from different subfolders of the project. Related modules are presented on the figure:


### Script `check_ocn_pft.py`:
1. Open scripts and set your personal settings in section **User Settings**;
2. These scripts use several personal modules. Nevetheless, you should not change them and you have to adapt only **/settings/mcluster.py** or **/settings/mlocal.py** and use correct values in **logical_settings[0]** parameter from ***/settings/user_settings***. If you want to change colors you can do that in **/libraries/lib4colors.py** variable **check_colors**;
3. You can change PFT groups in sections: ***a.*** OCN -> Create OCN groups, ***b.*** ESA-CCI -> ESA groups;
4. Run scripts `python3 ./check_ocn_pft.py` and check your results in output folders.

The full list of personal modules which are presented in script:
- ***/libraries/lib4xarray*** -> module for data processing;
- ***/libraries/lib4sys_support*** -> module for work with file system;
- ***/libraries/lib4upscaling_support*** -> module for upscalling and downscalling burned area data;
- ***/libraries/lib4colors*** -> module with user settings for line colors;
- ***/settings/path_settings*** -> module for controlling work of **/settings/mcluster.py** or **/settings/mlocal.py**;
- ***/calc/lib4vis_control*** -> module for controlling work of **/libraries/lib4visualization.py**.

### Script `mpost4burn_area.py`:
1. Open script and set your personal settings in section **User Settings**. There are 2 options work script work: 1 - *OCN* input data, 2 - *ESA-CCI MODIS* input data;
2. These scripts use several personal modules. Nevetheless, you should not change them and you have to adapt only **/settings/mcluster.py** or **/settings/mlocal.py** and use correct values in **logical_settings[0]** parameter from ***/settings/user_settings***.
3. Run scripts `python3 ./mpost4burn_area.py` and check your results in output folders.
Important: You output path should be the same as input data paths for script `fire_xarray.py` or you can copy output data in correct folder later.

The full list of personal modules which are presented in script:
- ***/libraries/lib4sys_support*** -> module for work with file system;
- ***/libraries/lib4postprocessing*** -> module for data processing;
- ***/settings/path_settings*** -> module for controlling work of **/settings/mcluster.py** or **/settings/mlocal.py**;

### Script `run_ocn_postprocessing.sh`:
1. Open script and set correct values in section **User settings**;
2. Run script `./run_ocn_postprocessing.sh`
3. Check results







[1]: https://git.bgc-jena.mpg.de/szaehle/ocn-v2/-/blob/reccap2a_ocn_updates_v202302/OCN_running_scripts/create_trendy_output_fire.sh