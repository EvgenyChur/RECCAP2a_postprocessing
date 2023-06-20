# Scripts description:

Scripts from this folder has the main purpose which is related to downloading data from output source and preprocessing of such data for further use in OCN model, data analysis and ets.

1. **Group 1: Preprocessing of ESA-CCI MODIS v5.0 data:**

This group was created for preprocessing of ESA-CCI MODIS v5.0 data and consists of three scripts:
- `prep_ESA.py` -> the main script with ESA-CCI MODISv5.0 preprocessing algorithm; This script is important because we use the ouptup results as a main source of fire data for OCN model. P.S.: You can get correct values from this script only on the MPI-BGC claster, due to several additional bash scripts;
- `unzip_ESA.sh` -> unzipping of raw ESA-CCI MODIS v5.0 data;
- `postprocess_ESA.sh` -> changing special attributes in preprocessed ESA-CCI MODIS v5.0 data for reading them into OCN model;

The main results of this group of scripts are the yearly NetCDF files (***lfire_frac_{year}.nc***) with monthly information about ESA-CCI MODIS natural burned area fraction presented on OCN model grid. All NetCDF attributes were converted to readable for OCN model format and these files were used in OCN model as a source of satellite information (RECCAP2A).

| Burned area (grid = 0.25 deg) | Burned area (grid = 0.5 deg) |  Line plot |
|:-----------------------------:|:----------------------------:|:----------:|
| ![][fig1a]                    | ![][fig1b]                   | ![][fig1c] |

[fig1a]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/PREPROCESS/PREP_ESA/baf_esa025_2001.png
[fig1b]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/PREPROCESS/PREP_ESA/baf_esa05_2001.png
[fig1c]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/PREPROCESS/PREP_ESA/fire_com.png

2. **Group 2. Preprocessing GFED data:**

This group was created for preprocessing of GFED data and consists of three scripts:
- `run_get_GFED.sh` -> running script of `get_GFED.py`;
- `get_GFED.py` -> script for downloading GFED data;
- `read_GFED_data.py` -> intial preprocessing of raw GFED data.

Previously, we used `GFED4.1s` data, but this dataset has data from 2001 - 2016. The new datasep has name `GFED` based on *GFED4.1s* data and has data from 2001 - 2020. More information about dataset you can find [here][1].

[1]: https://gmd.copernicus.org/articles/15/8411/2022/gmd-15-8411-2022-discussion.html


3. **Group 3. Preprocessing LAI data:**

This group was created for preprocessing of LAI data based on different datasets (LTDR, MODIS, GLOBMAP) to the special format is appropriate for OCN model. Group consists of two scripts:
- `prep_LAI.py` -> main preprocessing script;
- `yearmean_lai.py` -> auxiliary script for LTDR dataset.

![result_3](https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/PREPROCESS/collage_lai_diff.png)

## How to set and use scripts:
1. **Group 1: Preprocessing of ESA-CCI MODIS v5.0 data:**
    - Open the main script for preprocessing of ESA-CCI MODIS data (***/preprocessing/prep_ESA.py***) and use your parameters in section **Users settings**, where you can control:
        * *logical parameters* -> allow you to turn on and off different parts of the preprocessing algorithm;
        * *parameters for output results* -> input and output parameters depending on your working machine (*local* or *cluster*). You can set correct data paths in **/settings/mlocal.py** or **/settings/mcluster.py**. The ***/settings/path_settings.py*** module has control functions and you don't need to change it. More information, how to set input and output parameteres you can find in a corresponding readme file (**/settings/readme.mk**);
        * *settings for plots* -> plot parameters, you can use current values;
        * *settings for time* -> we have raw ESA-CCI MODIS v5.0 data from 2001 to 2020 years, because of that you can use years for analysis only in this time period. Actual on 05.06.2023 (maybe later we will be able more data);
        * *additional settings* -> you can ignore *section 2.5* and if you use cluster don't forget to check paths of shell scripts.

    In addition to **User settings** section of this script there are two additional modules with setting which you have to check before start:
        *  -> get information about input and output data paths. You have to check it and use correct paths for output results. Script uses two different output paths: for NetCDF data and for control figures;
        * ***/settings/user_settings.py*** -> you have to check values only in *logical_settings* variable. In particular, you have to change only `logical_settings[0]` parameter.

    - Important only if `logical_settings[0] = True`:
        * if you want to use raw ESA-CCI MODIS v5.0 data you can unzip them using this script. Open script (***/preprocessing/prep_ESA.py***) and check values in **User settings**. If you already have unpacked data, you can ignore this script and use `zero = False` into ***/preprocessing/prep_ESA.py***;
        * If you want to use preprocessed data as a source of initial information for OCN model you have to use ***/preprocessing/postprocess_ESA.py***. Open script (***/preprocessing/prep_ESA.py***) and check values in **User settings**. Script uses results prepared on the previous steps.

    After that, you have to save you changes and run script:
    ```
    python3 ./preprocessing/prep_ESA.py
    ```

2. **Group 2. Preprocessing GFED data:**
    - Open running script ***/preprocessing/run_get_GFED.sh*** and check settings in section **User settings**. Generally, you have change only output path.
    - Open script `get_GFED.py`. You don't need to change parameters in this script, but you have to check that you have module `urllib`. Otherwise, you have to install it:
    ```
    conda install -c anaconda urllib3
    ```
    then you can run running script:
    ```
    ./preprocessing/run_get_GFED.sh
    ```
    - Open scrip `read_GFED_data.py` and check parameters from **User settings**. Generally, you have to change only `mpath`. Save changes and run script:
    ```
    ./preprocessing/read_GFED_data.sh
    ```
    Now, you can use updated GFED data. Preprocessed data have the sae format as GFED data.

3. **Group 3. Preprocessing LAI data:**
    - Open script ***/preprocessing/prep_LAI.py*** and set correct values in section **User settings**. Save changes. If you want additionally use auxiliary script for LTDR dataset, you should check **User settings** in shell script. Then, you can run it.
    ```
    ./preprocessing/prep_LAI.py
    ```


