# -*- coding: utf-8 -*-
"""
The module has user settings for visualization:

The full list of OCN simulations:
    Fire simulations prepared by Ana Bastos: 
        OCN_S2.1, OCN_S2.2, OCN_S2.1.1, OCN_S3.1, OCN_S3.2
        
    None fire simulations prepared by Ana Bastos:
        'OCN_S2.1_nf', 'OCN_S3.1_nf'
    
    Fire simulations prepared by Evgenii Churiulin *(v202210) ERA5 (1950 - 2020)
        'OCN_S0'    , 'OCN_S2Prog'   , 'OCN_S2Diag'   ,
        
    Fire simulations prepared by evgenii Churiulin *(v202303) ERA5 (1960 - 2022)
        'OCN_S0_v3' , 'OCN_S2Prog_v3', 'OCN_S2Diag_v3', 'OCN_Spost_v3'

Important: Most of the scipts use these user settings. Most of them use
           logical_settings[0] or logical_settings[1]. At the same time, script
           **/main_fire_xarray.py** use all of them. The full list of scripts
           where this module was used see below:
        Script (module)                         Settings
 1. /settings/path_settings.py      --> logical_settings

 2. /calc/vis_controls.py           --> time_limits, plt_limits, clb_limits,
                                        layout_settings, clb_diff_limits
 3. /calc/one_point.py              --> stations, plt_limits_point

 4. /preprocessing/prep_ESA.py      --> logical_settings
 5. /preprocessing/prep_LAI.py      --> logical_settings, domain_lim

 6. /libraries/lib4xarray.py        --> time_limits, domain_lim, psets
 7. /libraries/lib4visualization.py --> stations

 8. /main/ba_esa_pft.py             --> logical_settings
 9. /main/landcover.py              --> logical_settings, time_limits, stations
10. /main/check_ocn_pft.py          --> logical_settings, time_limits
11. /main/fire_xarray.py            --> all user settings
12. /main/fire_ratio.py             --> logical_settings, time_limits
14. /main/check_ESA_tbaf.py         --> logical_settings

15. /test/ctr4ocn_out.py            --> logical_settings
16. /test/2dmap4sites.py            --> stations

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  561 804-6142
email:  evchur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-07-02 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-09-23 Evgenii Churiulin, MPI-BGC
           Updated the module. All settings for users were relocated
           to this module
    1.3    2023-03-17 Evgenii Churiulin, MPI-BGC
           Module was updated.
    1.4    2023-05-08 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
import sys

# =============================   Personal functions   ==================

# ================   User settings (have to be adapted)  ================

# Section 1: Main settings:
# ======================================================================
# -- format of output figures
form4out_fig = 'png'
# -- The first year which you want to use in your linear plot
start_year = 2003   # limits for y and x axis of linear plots depend on it. See below: 1980

# -- 1.1: Set logical parameters for computations: Most of the scripts from this
#         project use logical_settings[0] or logical_settings[1] as key parameters
#         for understanding which computer (cluster or local) and settings should
#         be active and do you want to get more information about NetCDF.
#         You can find the full list of script where this module is active, above:
yes = True
no  = False
 
logical_settings = [
    #-- 0. Do you want to calculate on cluster?                      --> lcluster (yes / no)
    yes,
    #-- 1. Do you want to get more information about NetCDF data?    --> lnc_info (yes / no)
    no,
    #-- 2. Do you want to get values for stations?                   --> station_mode (yes / no)
    no,
    #-- 3. Do you want to visualize data (line plots)?               --> lvis_lines (yes / no)
    no,
    #-- 4. Do you want to visualize data on grid for one moment?     --> lBasemap_moment (yes / no)
    yes,
]

# -- 1.2: Additional settings for running **\main\fire_xarray.py**:
#         You can don't change them. Parameters are active if lBasemap_moment = TRUE
calculation_settings = [
    #-- 0. Activate algorithm for mean calculations?                 --> lmean_calc (yes / no)
    yes,
    #-- 1. Activate algorithm for std calculations?                  --> lstd_calc (yes / no)
    yes,  
    #-- 2. Activate algorithm for trends calculations?               --> ltrend_calc (yes / no)
    yes,  
    #-- 3. Activate algorithm for difference calculations?           --> ldiff_calc (yes / no)
    yes,
    #-- 4. Activate algorithm for mean visualization (one figure)?   --> lmean_plot (yes / no)
    no,
    #-- 5. Activate algorithm for std visualization (one figure)?    --> lstd_plot (yes / no)
    no,
    #-- 6. Activate algorithm for trends visualization (one figure)? --> ltrend_plot (yes / no)
    no,
    #-- 7. Activate algorithm for collage plots:
    #  (1st row - mean, 2nd row - std, 3rd  row - trend)?            --> lcollage (yes / no)
    yes, 
    #-- 8. Activate algorithm for difference plots
    #   (1st row - mean, 2nd row - std, 3rd  row - trend)?           --> ldiff_plot (yes / no)
    yes,
]

# -- 1.4: Select available datasets (OCN simulations and datasets). Settings active
#    for running **\main\fire_xarray.py**
'''
Available datasets full list:
    1. burned area --> OCN, JULES, ORCHIDEE models results and datasets:
        a. ESA-CCI MODIS v5.0    -> 'BA_MODIS' -> 2001 - 2018 and 2001 - 2020
        b. ESA-CCI L4 AVHRR-LTDR -> 'BA_AVHRR' -> 1982 - 2018
        c. 'GFED4.1s'            ->            -> 2001 - 2016
        d. 'GFED_TOT'            ->            -> 2001 - 2020
        e. 'GFED_FL'             ->            -> 2001 - 2020
    2. fFire       --> OCN, JULES, ORCHIDEE models results and datasets: 
        a. 'GFED4.1s'            ->            -> 2001 - 2016
        b. 'GFED_AG_TOT'         ->            -> 2001 - 2020
        c. 'GFED_BG_TOT'         ->            -> 2001 - 2020
        d. 'GFED_AG_FL'          ->            -> 2001 - 2020
        e. 'GFED_BG_FL'          ->            -> 2001 - 2020
    3. lai         --> OCN, JULES, ORCHIDEE model results and datasets:
        a. 'LAI_LTDR'            ->            -> 1981 - 2020
        b. 'LAI_MODIS'           ->            -> 2000 - 2020
        c. 'GLOBMAP'             ->            -> 1982 - 2020
    4. cVeg        --> OCN, JULES, ORCHIDEE models results and datasets:
        a.
    5. npp         --> OCN, JULES  models results and datasets: 
        a. 'MOD17A3HGFv061'      ->            -> 2000 - 2020
    6. gpp         --> OCN, JULES, ORCHIDEE models results and datasets: 
        a. 'MOD17A2HGFv061'      ->            -> 2000 - 2020
        b. 'MOD17A3HGFv061'      ->            -> 2000 - 2020
    7. nee         --> OCN,  models results and datasets: 
        a.
    8. nbp         --> OCN, JULES, ORCHIDEE models results and datasets: 
        a.
'''
# -- OCN simulations:
ocn_sim = ['OCN_S2Prog_v3', 'OCN_S2Diag_v3']
# -- JULES simulations:
jul_sim = ['JUL_S2Prog', 'JUL_S2Diag']
# -- ORCHIDEE simulations: 
orc_sim = ['ORC_S2Prog', 'ORC_S2Diag']

# -- 1.4.1: Select datasets which you want to figure out on your linear plots
if (logical_settings[3] == True) and (logical_settings[4] == False):
    # Available datasets for data processing and visualization (linear plot)
    av_datasets = {
        'burned_area' : ocn_sim + jul_sim + orc_sim + ['BA_MODIS', 'GFED4.1s', 'GFED_TOT'],
        'fFire'       : ocn_sim + jul_sim + orc_sim + ['GFED4.1s'],   
        'lai'         : ocn_sim + jul_sim + orc_sim + ['LAI_LTDR', 'GLOBMAP'],
        'cVeg'        : ocn_sim + jul_sim + orc_sim,
        'npp'         : ocn_sim + jul_sim,
        'gpp'         : ocn_sim + jul_sim + orc_sim,
        'nee'         : ocn_sim,
        'nbp'         : ocn_sim + jul_sim + orc_sim,
    }

    # Time ranges for OCN, JULES and ORCHIDEE models (time range - free)
    set4time = {
        'OCN' : [start_year, 2020], # 1980
        'JUL' : [start_year, 2020], # 1980
        'ORC' : [start_year, 2020], # 1980
    }
else:
    if (logical_settings[3] == False) and (logical_settings[4] == True):
        print('Your are going to create 2D plots!. lvis_lines was turned off')
    else:
        print('Linear plot and basemap mode were activated together. Stop')
        sys.exit()        

# -- 1.4.2: Select datasets which you want to figure out on your 2D maps
if (logical_settings[3] == False) and (logical_settings[4] == True):
    # Available datasets for data processing and visualization (2D plot)
    av_datasets = {
        'burned_area' : ['JUL_S2Prog', 'ORC_S2Prog'] + ocn_sim + ['BA_MODIS', 'GFED_TOT'],
        'fFire'       : ['JUL_S2Prog', 'ORC_S2Prog'] + ocn_sim + ['GFED4.1s'],         
        'lai'         : ['JUL_S2Prog', 'ORC_S2Prog'] + ocn_sim + ['LAI_LTDR', 'GLOBMAP'],
        'cVeg'        : ['JUL_S2Prog', 'ORC_S2Prog'] + ocn_sim,
        'npp'         : ['JUL_S2Prog'              ] + ocn_sim,
        'gpp'         : ['JUL_S2Prog', 'ORC_S2Prog'] + ocn_sim,
        'nee'         :                                ocn_sim,
        'nbp'         : ['JUL_S2Prog', 'ORC_S2Prog'] + ocn_sim,
    }

    # (time scale -> should be the same for each dataset - 2003 - 2016)
    set4time = {
        'OCN' : [2003, 2020],
        'JUL' : [2003, 2020],
        'ORC' : [2003, 2020],
    }
else:
    if (logical_settings[3] == True) and (logical_settings[4] == False):
        print(('Your are going to create linear plots!.'
               ' lBasemap_moment was turned off'))
    else:
        print('Linear plot and basemap mode were activated together. Stop')
        sys.exit()

# -- 1.5: Datasets have different time perios. You have to choose your time
#         periods for datasets. Also, the x-axis limits for linear plots depending
#         on OCN values.

# -- Time limits for simulations depending on parameter for research
time_limits = {
      'burned_area' : {
      # --  datasets                       time period
          'GFED4.1s' : [         2003          ,          2016          ],     # was 2001 - 2016
          'GFED_TOT' : [         2003          ,          2020          ],
          'GFED_FL'  : [         2003          ,          2020          ], 
          'BA_MODIS' : [         2003          ,          2020          ],     # was 2001 - 2020
          'BA_AVHRR' : [         2003          ,          2016          ],     # was 2001 - 2020
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],     # use 2001 - 2016 for landcover
          'JUL'      : [ set4time.get('JUL')[0], set4time.get('JUL')[1] ],
          'ORC'      : [ set4time.get('ORC')[0], set4time.get('ORC')[1] ],
      },
      'fFire'       : {
          'GFED4.1s' : [         2003          ,          2020          ],
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],     # was 2001 - 2016
          'JUL'      : [ set4time.get('JUL')[0], set4time.get('JUL')[1] ],
          'ORC'      : [ set4time.get('ORC')[0], set4time.get('ORC')[1] ],
      },
      'lai'         : {
          'LAI_LTDR' : [         2003          ,          2018          ],
          'LAI_MODIS': [         2003          ,          2020          ],
          'GLOBMAP'  : [         2003          ,          2020          ],
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],     # was 2001 - 2016
          'JUL'      : [ set4time.get('JUL')[0], set4time.get('JUL')[1] ],
          'ORC'      : [ set4time.get('ORC')[0], set4time.get('ORC')[1] ],
      },
      'cVeg'        : {
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],     # was 1980 - 2020
          'JUL'      : [ set4time.get('JUL')[0], set4time.get('JUL')[1] ],
          'ORC'      : [ set4time.get('ORC')[0], set4time.get('ORC')[1] ],
      },
      'npp'         : {
          'MOD17A3'  : [         2001          ,          2020          ],
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],
          'JUL'      : [ set4time.get('JUL')[0], set4time.get('JUL')[1] ],
      },
      'gpp'         : {
          'MOD17A2'  : [         2003          ,          2020          ],
          'MOD17A3'  : [         2003          ,          2020          ],
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],
          'JUL'      : [ set4time.get('JUL')[0], set4time.get('JUL')[1] ],
          'ORC'      : [ set4time.get('ORC')[0], set4time.get('ORC')[1] ],
      },
      'nee' : {
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],
      },
      'nbp' : {
          'OCN'      : [ set4time.get('OCN')[0], set4time.get('OCN')[1] ],
          'JUL'      : [ set4time.get('JUL')[0], set4time.get('JUL')[1] ],
          'ORC'      : [ set4time.get('ORC')[0], set4time.get('ORC')[1] ],
      },
}

# -- 1.6: Settings for difference metrics (diff = refer - comp_ds)
if ((logical_settings[4] == True) and (calculation_settings[3] == True)):
    # -- OCN reference simulation
    ocn_refer   = 'OCN_S2Prog_v3' # 'OCN_S0'       
    # -- OCN research  simulation
    ocn_comp_ds = 'OCN_S2Diag_v3' # 'OCN_S2Prog'

    # Define datasets:
    diff_options = {
    #     parameter        refer       comp_ds         Possible options
        #'burned_area' : ['GFED4.1s', 'OCN_S3.1'  ],   # see dataset name from av_datasets 
        #'fFire'       : ['GFED4.1s', 'OCN_S3.1'  ],  
        #'lai'         : ['GLOBMAP' , 'OCN_S3.2'  ],
        'burned_area' : ['BA_MODIS', ocn_comp_ds ],
        'fFire'       : ['GFED4.1s', ocn_comp_ds ],    
        'lai'         : [ocn_refer , ocn_comp_ds ],
        'cVeg'        : [ocn_refer , ocn_comp_ds ],
        'npp'         : [ocn_refer , ocn_comp_ds ],
        'gpp'         : [ocn_refer , ocn_comp_ds ],
        'nee'         : [ocn_refer , ocn_comp_ds ],
        'nbp'         : [ocn_refer , ocn_comp_ds ],
    }

# -- 1.7: Additional settings for OCN simulations (have strange time format due to
#         we have to set the correct time format manually):
# Time ranges for OCN simulations:
psets = {
    # OCN simulations based on Ana's Bastos experiment:
    'OCN_S2.1'      : ['1950-01-01', '2022-01-01', '1M' ],
    'OCN_S2.2'      : ['1950-01-01', '2022-01-01', '1M' ],
    'OCN_S3.1'      : ['1950-01-01', '2022-01-01', '1M' ],
    'OCN_S3.2'      : ['1950-01-01', '2022-01-01', '1M' ],
    'OCN_S2.1_nf'   : ['1950-01-01', '2022-01-01', '1M' ],
    'OCN_S3.1_nf'   : ['1950-01-01', '2022-01-01', '1M' ],
    'OCN_S2.1.1'    : ['1950-01-01', '2023-01-01', '1M' ],
    # OCN simulations based on RECCAP_v1 experiment
    'OCN_S0'        : ['1950-01-01', '2021-01-01', '1M' ],
    'OCN_S2Prog'    : ['1950-01-01', '2021-01-01', '1M' ],
    'OCN_S2Diag'    : ['2000-01-01', '2021-01-01', '1M' ],
    # OCN simulations based on RECCAP_v3 experiment
    'OCN_Spost_v3'  : ['1850-01-01', '2021-01-01', '1M' ],
    'OCN_S0_v3'     : ['1960-01-01', '2021-01-01', '1M' ],
    'OCN_S2Prog_v3' : ['1960-01-01', '2023-01-01', '1M' ], # was 2021-01-01
    'OCN_S2Diag_v3' : ['2003-01-01', '2021-01-01', '1M' ],
    # ORCHIDEE simulations
    'ORC_S0'        : ['1960-01-01', '2021-01-01', '1M' ],
    'ORC_S2Prog'    : ['1960-01-01', '2021-01-01', '1M' ],
    'ORC_S2Diag'    : ['2003-01-01', '2021-01-01', '1M' ],
    # Other datasets
    'NDEP'          : ['2018-01-01', '2018-12-01', '1MS'],
}

# Section 2: Domain settings:
# ======================================================================
# -- 2.1: Datasets have different spatial resolution. For example: the datasets
#         MODIS, AVHRR and GFED have grids: lat (-90 : 90) and lon (-180 : 180),
#         however the OCN grids are: (-60 : 90) and (-180 : 180). Because of that
#         it is really important to get the simular coordinates
#         before - interpolation. Otherwise, the model grid will be irregular.
domain_lim = {
    # Domain    lat start  lat stop  lon start   lon stop
    'Global' : [   90.0  ,   -60.0 ,   -180.0 ,   180.0  ],
    'Europe' : [   72.0  ,    34.0 ,    -10.0 ,    45.0  ],
    'Tropics': [   23.0  ,   -23.0 ,   -180.0 ,   180.0  ],
    'NH'     : [   80.0  ,    30.0 ,   -180.0 ,   180.0  ],
    'Other'  : [   90.0  ,   -90.0 ,   -180.0 ,   180.0  ]
}

# Section 3: Station settings:
# ======================================================================
# -- 3.1: There is option for analysis of data in a special point.
#         You can add your point in this section.
stations  = {
# Point     lat    lon   Place                           PFT
    1 : [   2.7,  -65.5, 'SA1'  , 'TrBE - 100%'                             ],
    2 : [  -7.8,  -45.8, 'SA2'  , 'HC4  - 62.9%, TrBR - 28.2%, TrBE -  4.8%'],
    3 : [ -19.7,  -50.3, 'SA3'  , 'HC4  - 51.9%, TrBR - 19.0%, BS   - 11.2%'],
    4 : [  42.5, -100.0, 'NA1'  , 'HC3  - 57.9%, CC3  - 24.9%, CC4  - 11.1%'],
    5 : [  38.4,   -8.1, 'PORT' , 'CC3  - 49.7%, HC4  - 19.2%, TeBS - 18.9%'],
    6 : [  51.1,   68.5, 'KAZ'  , 'HC3  - 78.1%, CC3  - 21.5%, BBS  -  0.2%'],
    7 : [  51.1,  112.5, 'RUS1' , 'BNE  - 52.0%, HC3  - 36.3%, BBS  -  7.1%'],
    8 : [  48.2,  114.5, 'MONG' , 'HC3  - 100%'                             ],
    9 : [   8.5,    6.5, 'AFR1' , 'HC4  - 62.6%, TrBR - 16.8%, CC3  - 14.4%'],
    10: [  -1.5,   24.6, 'AFR2' , 'TrBE - 100%'                             ],
    11: [ -24.2,   21.7, 'AFR3' , 'HC4  - 73.6%, TeBE -  7.7%, TeBS -  7.7%'],
    12: [ -20.8,   46.2, 'MAD'  , 'HC4  - 87.3%, TrBR -  6.7%, HC3  -  4.6%'],
    13: [ -17.4,  132.4, 'AST1' , 'TrBR - 33.1%, HC4  - 28.7%, TeBE - 24.4%'],
    14: [ -24.1,  125.4, 'AST2' , 'HC4  - 53.0%, TeBE - 20.4%, TeBS - 20.4%'],
    15: [ -26.9,  148.8, 'AST3' , 'HC4  - 65.6%, TeBS - 12.1%, TeBE - 11.4%'],
    16: [  17.3,   77.2, 'IND1' , 'CC3  - 46.5%, CC4  - 18.5%, TrBR - 16.3%'],
    17: [  17.9,   95.4, 'BIRM' , 'TrBR - 40.8%, CC3  - 39.8%, HC4  - 12.1%'],
}  

# Section 4: Plot settings:
# ======================================================================
# -- 4.1 Settings for linear plots:
if (start_year >= 1960) and (start_year < 1980):
    # Settings for linear plots splited by region. Time --> 1960 - 2022
    print(('Using plot settings (set 1).'
          ' Settings actual for period since 1960 to 2022'))
    plt_limits = {
        # Region      Mode             ymin      ymax     ystep
        'Global' : {'burned_area' : [  2000.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   400.0,   650.1,   25.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   110.0,   200.1,   10.0 ],
                    'npp'         : [    60.0,   100.1,    5.0 ],
                    'nee'         : [    -7.0,     0.1,    1.0 ],
                    'nbp'         : [    -2.0,     6.1,    1.0 ],
                    'fFire'       : [     0.0,     7.1,    1.0 ],
        },
        'Europe' : {'burned_area' : [     0.0,   140.1,   10.0 ],
                    'cVeg'        : [    20.0,    60.1,    5.0 ],
                    'lai'         : [     0.0,     3.6,    0.5 ],
                    'gpp'         : [     5.0,    14.51,   0.5 ],
                    'npp'         : [     5.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.01,   0.2 ],
                    'nbp'         : [    -1.0,     0.81,   0.2 ],
                    'fFire'       : [     0.0,     0.17,   0.02],
        },  
        'Tropics': {'burned_area' : [  2500.0,  9500.1, 1000.0 ],
                    'cVeg'        : [   200.0,   400.1,   25.0 ],
                    'lai'         : [     0.0,     1.21,   0.1 ],
                    'gpp'         : [    60.0,   130.1,   10.0 ],
                    'npp'         : [    30.0,    70.1,    5.0 ],
                    'nee'         : [    -4.0,     2.1,    1.0 ],
                    'nbp'         : [    -5.0,     4.1,    1.0 ],
                    'fFire'       : [     0.0,     6.1,    1.0 ],
        },
        # (not optimized)
        'NH'     : {'burned_area' : [   200.0,  1200.1,  200.0 ],
                    'cVeg'        : [    20.0,    40.1,    5.0 ],
                    'lai'         : [     0.0,     3.1,    0.2 ],
                    'gpp'         : [    10.0,    15.1,    1.0 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.5,    0.2 ],
                    'nbp'         : [    -0.2,     1.5,    0.2 ],
                    'fFire'       : [     0.0,     0.2,    0.02],
        },
        # (not optimized)       
        'Other'  : {'burned_area' : [  3500.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   450.0,   750.1,   50.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   180.1,   10.0 ],
                    'npp'         : [    65.0,    95.1,    5.0 ],
                    'nee'         : [    -7.0,     3.1,    1.0 ],
                    'nbp'         : [    -4.0,     8.1,    2.0 ],
                    'fFire'       : [     0.0,     8.1,    2.0 ],
        },
    }

    # -- Settings for station plots
    plt_limits_point  = {
        #     Mode           ymin      ymax     ystep
        'burned_area' : [     0.0,     4.1,    0.5  ],
        'cVeg'        : [     0.0,     6.1,    0.25 ],
        'lai'         : [     0.0,     6.1,    0.5  ],
        'gpp'         : [     0.0,     3.51,   0.25 ],
        'npp'         : [     0.0,     2.1,    0.5  ],
        'nee'         : [    -0.6,     0.61,   0.2  ],
        'nbp'         : [    -0.4,     0.41,   0.2  ],
        'fFire'       : [     0.0,     0.31,   0.05 ],
    }

elif (start_year >= 1980) and (start_year < 2001):
    # Settings for linear plots splited by region. Time --> 1980 - 2022
    print(('Using plot settings (set 2).'
          ' Settings actual for period since 1980 to 2022'))
    plt_limits = {
        # Region      Mode             ymin      ymax     ystep  
        'Global' : {'burned_area' : [  2000.0, 11000.1, 1000.0 ],
                    'cVeg'        : [   400.0,   675.1,   25.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   200.1,   10.0 ],
                    'npp'         : [    70.0,   105.1,    5.0 ],
                    'nee'         : [    -7.0,    -2.1,    0.5 ],
                    'nbp'         : [    -4.0,     6.1,    2.0 ],
                    'fFire'       : [     0.0,     5.1,    1.0 ],
        },
        'Europe' : {'burned_area' : [     0.0,   200.1,   20.0 ],
                    'cVeg'        : [    20.0,    65.1,    5.0 ],
                    'lai'         : [     0.0,     3.6,    0.5 ],
                    'gpp'         : [     5.0,    15.1,    2.5 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,    -0.21,   0.2 ],
                    'nbp'         : [    -0.6,     0.81,   0.2 ],
                    'fFire'       : [     0.0,     0.17,   0.02],
        },
        'Tropics': {'burned_area' : [  2500.0,  9500.1, 1000.0 ],
                    'cVeg'        : [   200.0,   400.1,   25.0 ],
                    'lai'         : [     0.0,     1.21,   0.1 ],
                    'gpp'         : [    70.0,   130.1,   10.0 ],
                    'npp'         : [    34.0,    60.1,    5.0 ],
                    'nee'         : [    -4.0,     0.1,    1.0 ],
                    'nbp'         : [    -6.0,     4.1,    1.0 ],
                    'fFire'       : [     0.0,     5.1,    1.0 ]
        }, 
        # (not optimized)         
        'NH'     : {'burned_area' : [   200.0,  1200.1,  200.0 ],
                    'cVeg'        : [    20.0,    40.1,    5.0 ],
                    'lai'         : [     0.0,     3.1,    0.2 ],
                    'gpp'         : [    10.0,    15.1,    1.0 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.5,    0.2 ],
                    'nbp'         : [    -0.2,     1.5,    0.2 ],
                    'fFire'       : [     0.0,     0.2,    0.02],
        }, 
        # (not optimized)       
        'Other'  : {'burned_area' : [  3500.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   450.0,   750.1,   50.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   180.1,   10.0 ],
                    'npp'         : [    65.0,    95.1,    5.0 ],
                    'nee'         : [    -7.0,     3.1,    1.0 ],
                    'nbp'         : [    -4.0,     8.1,    2.0 ],
                    'fFire'       : [     0.0,     8.1,    2.0 ],
        },
    }

    # -- Settings for station plots
    plt_limits_point  = {
        #     Mode              ymin      ymax     ystep
        'burned_area' : [     0.0,     4.1,    0.5  ],
        'cVeg'        : [     0.0,     1.25,   0.05 ],
        'lai'         : [     0.0,     6.1,    0.5  ],
        'gpp'         : [     0.0,     3.51,   0.25 ],
        'npp'         : [     0.0,     2.1,    0.5  ],
        'nee'         : [    -0.6,     0.61,   0.2  ],
        'nbp'         : [    -0.4,     0.41,   0.2  ],
        'fFire'       : [     0.0,     0.31,   0.05 ],
    }

elif (start_year >= 2001):
    # Settings for linear plots splited by region. Time --> 2001 - 2022
    print(('Using plot settings (set 3).'
          ' Settings actual for period since 2001 to 2022'))    
    plt_limits = {
        # Region      Mode             ymin      ymax     ystep
        'Global' : {'burned_area' : [  2000.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   400.0,   650.1,   25.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   130.0,   250.1,   10.0 ],
                    'npp'         : [    70.0,   100.1,    5.0 ],
                    'nee'         : [    -7.0,    -2.1,    1.0 ],
                    'nbp'         : [    -2.0,     5.1,    1.0 ],
                    'fFire'       : [     0.0,     5.1,    1.0 ],
        },
        'Europe' : {'burned_area' : [     0.0,   180.1,   20.0 ],
                    'cVeg'        : [    30.0,    70.1,   10.0 ],
                    'lai'         : [     0.0,     3.6,    0.5 ],
                    'gpp'         : [     6.0,    14.51,   0.5 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.01,   0.2 ],
                    'nbp'         : [    -1.0,     0.81,   0.2 ],
                    'fFire'       : [    -0.05,    0.21,   0.05],
        },   
        'Tropics': {'burned_area' : [  2500.0,  9500.1, 1000.0 ],
                    'cVeg'        : [   200.0,   400.1,   25.0 ],
                    'lai'         : [     0.0,     1.21,   0.1 ],
                    'gpp'         : [    70.0,   150.1,   10.0 ],
                    'npp'         : [    35.0,    70.1,    5.0 ],
                    'nee'         : [    -4.0,     0.1,    1.0 ],
                    'nbp'         : [    -5.0,     3.1,    1.0 ],
                    'fFire'       : [     0.0,     4.1,    1.0 ],
        },
        # (not optimized)
        'NH'     : {'burned_area' : [   200.0,  1200.1,  200.0 ],
                    'cVeg'        : [    20.0,    40.1,    5.0 ],
                    'lai'         : [     0.0,     3.1,    0.2 ],
                    'gpp'         : [    10.0,    15.1,    1.0 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.5,    0.2 ],
                    'nbp'         : [    -0.2,     1.5,    0.2 ],
                    'fFire'       : [     0.0,     0.2,    0.02],
        },
        # (not optimized)
        'Other'  : {'burned_area' : [  3500.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   450.0,   750.1,   50.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   180.1,   10.0 ],
                    'npp'         : [    65.0,    95.1,    5.0 ],
                    'nee'         : [    -7.0,     3.1,    1.0 ],
                    'nbp'         : [    -4.0,     8.1,    2.0 ],
                    'fFire'       : [     0.0,     8.1,    2.0 ],
        },
    }

    # -- Settings for station plots
    plt_limits_point  = {
        #    Mode           ymin      ymax     ystep
        'burned_area' : [     0.0,     4.1,    0.5  ],
        'cVeg'        : [     0.0,     6.1,    0.25 ],
        'lai'         : [     0.0,     6.1,    0.5  ],
        'gpp'         : [     0.0,     3.51,   0.25 ],
        'npp'         : [     0.0,     2.1,    0.5  ],
        'nee'         : [    -0.6,     0.61,   0.2  ],
        'nbp'         : [    -0.4,     0.41,   0.2  ],
        'fFire'       : [     0.0,     0.31,   0.05 ],
    }  
else:
    print(('Your time range is unavailable.'
          ' Please add a new one or correct data in parameter --> start_year'))
    sys.exit()

# -- 4.2: Settings for 2D plots (normal mode):
# Actual matplotlib colormap are here:
#    https://matplotlib.org/stable/tutorials/colors/colormaps.html

# -- Colorbar settings for data over 'Global', 'Tropics', 'Other' regions:
clb_limits_GTO = [
    # Fire datasets
    {'mode':'burned_area', 'param':'mean' , 'ymin':  0.0  , 'ymax':     0.30 , 'cbar' : 'hot_r'       }, # Initial  0.0, 0.30 
    {'mode':'burned_area', 'param':'std'  , 'ymin':  0.0  , 'ymax':     0.10 , 'cbar' : 'hot_r'       }, # Initial  0.0, 0.15
    {'mode':'burned_area', 'param':'trend', 'ymin': -1e-3 , 'ymax':     1e-3 , 'cbar' : 'RdBu_r'      },
    # Carbon in vegetation
    {'mode':'cVeg'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':    20.0  , 'cbar' : 'gist_earth_r'},
    {'mode':'cVeg'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':     2.0  , 'cbar' : 'gist_earth_r'},
    {'mode':'cVeg'       , 'param':'trend', 'ymin': -0.04 , 'ymax':     0.04 , 'cbar' : 'RdBu_r'      }, 
    # Gross Primary Production
    {'mode': 'gpp'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':   4000.0 , 'cbar' : 'gist_earth_r'},
    {'mode': 'gpp'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':    400.0 , 'cbar' : 'gist_earth_r'},
    {'mode': 'gpp'       , 'param':'trend', 'ymin':-10.0  , 'ymax':     10.0 , 'cbar' : 'RdBu_r'      },
    # Net primary production                
    {'mode': 'npp'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':  1500.0  , 'cbar' : 'gist_earth_r'},
    {'mode': 'npp'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':   200.0  , 'cbar' : 'gist_earth_r'},
    {'mode': 'npp'       , 'param':'trend', 'ymin':-10.0  , 'ymax':    10.0  , 'cbar' : 'RdBu_r'      },
    # Leaf Area Index
    {'mode': 'lai'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':     6.0  , 'cbar' : 'Greens'      },
    {'mode': 'lai'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':     3.0  , 'cbar' : 'Greens'      },
    {'mode': 'lai'       , 'param':'trend', 'ymin': -0.04 , 'ymax':     0.04 , 'cbar' : 'PRGn'        },
    # Net Ecosystem Exchange
    {'mode': 'nee'       , 'param':'mean' , 'ymin':-150.0 , 'ymax':    50.0  , 'cbar' : 'PRGn'        },
    {'mode': 'nee'       , 'param':'std'  , 'ymin':   0.0 , 'ymax':   200.0  , 'cbar' : 'Greens'      },
    {'mode': 'nee'       , 'param':'trend', 'ymin':  -2.0 , 'ymax':     2.0  , 'cbar' : 'RdBu_r'      },
    # Net Biome Production
    {'mode': 'nbp'       , 'param':'mean' , 'ymin': -60.0 , 'ymax':    60.0  , 'cbar' : 'PRGn'        },
    {'mode': 'nbp'       , 'param':'std'  , 'ymin':   0.0 , 'ymax':   150.0  , 'cbar' : 'Greens'      },
    {'mode': 'nbp'       , 'param':'trend', 'ymin':  -2.0 , 'ymax':     2.0  , 'cbar' : 'RdBu_r'      },
    # CO2 Flux to Atmosphere from Fire
    {'mode':'fFire'      , 'param':'mean' , 'ymin':  0.0  , 'ymax':    80.0  , 'cbar' : 'hot_r'       },
    {'mode':'fFire'      , 'param':'std'  , 'ymin':  0.0  , 'ymax':    60.0  , 'cbar' : 'hot_r'       },
    {'mode':'fFire'      , 'param':'trend', 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'RdBu_r'      }, 
]
  
# -- Colorbar settings for data over 'Europe', 'NH' regions:
clb_limits_EN = [
    # Fire datasets
    {'mode':'burned_area', 'param':'mean' , 'ymin':  0.0  , 'ymax':     0.05 , 'cbar' : 'hot_r'       }, # initial 0.0 0.08
    {'mode':'burned_area', 'param':'std'  , 'ymin':  0.0  , 'ymax':     0.03 , 'cbar' : 'hot_r'       }, # initial 0.0 0.01
    {'mode':'burned_area', 'param':'trend', 'ymin': -1e-4 , 'ymax':     1e-4 , 'cbar' : 'RdBu_r'      }, # -1e-5, 1e-5
    # Carbon in vegetation
    {'mode':'cVeg'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':    10.0  , 'cbar' : 'gist_earth_r'},
    {'mode':'cVeg'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':     1.5  , 'cbar' : 'gist_earth_r'},
    {'mode':'cVeg'       , 'param':'trend', 'ymin': -0.04 , 'ymax':     0.04 , 'cbar' : 'RdBu_r'      },
    # Gross Primary Production
    {'mode': 'gpp'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':  3000.0  , 'cbar' : 'gist_earth_r'},
    {'mode': 'gpp'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':   300.0  , 'cbar' : 'gist_earth_r'},
    {'mode': 'gpp'       , 'param':'trend', 'ymin':-10.0  , 'ymax':    10.0  , 'cbar' : 'RdBu_r'      },
    # Net primary production
    {'mode': 'npp'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':  1500.0  , 'cbar' : 'gist_earth_r'},
    {'mode': 'npp'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':   200.0  , 'cbar' : 'gist_earth_r'},
    {'mode': 'npp'       , 'param':'trend', 'ymin': -6.0  , 'ymax':     6.0  , 'cbar' : 'RdBu_r'      },
    # Leaf Area Index
    {'mode': 'lai'       , 'param':'mean' , 'ymin':  0.0  , 'ymax':     6.0  , 'cbar' : 'Greens'      },
    {'mode': 'lai'       , 'param':'std'  , 'ymin':  0.0  , 'ymax':     3.0  , 'cbar' : 'Greens'      },
    {'mode': 'lai'       , 'param':'trend', 'ymin': -0.03 , 'ymax':     0.03 , 'cbar' : 'PRGn'        },
    # Net Ecosystem Exchange
    {'mode': 'nee'       , 'param':'mean' , 'ymin':-100.0 , 'ymax':    50.0  , 'cbar' : 'PRGn'        },
    {'mode': 'nee'       , 'param':'std'  , 'ymin':   0.0 , 'ymax':   100.0  , 'cbar' : 'Greens'      },
    {'mode': 'nee'       , 'param':'trend', 'ymin':  -2.0 , 'ymax':     2.0  , 'cbar' : 'RdBu_r'      },
    # Net Biome Production
    {'mode': 'nbp'       , 'param':'mean' , 'ymin': -60.0 , 'ymax':    60.0  , 'cbar' : 'PRGn'        },
    {'mode': 'nbp'       , 'param':'std'  , 'ymin':   0.0 , 'ymax':   100.0  , 'cbar' : 'Greens'      },
    {'mode': 'nbp'       , 'param':'trend', 'ymin':  -2.0 , 'ymax':     2.0  , 'cbar' : 'RdBu_r'      },
    # CO2 Flux to Atmosphere from Fire
    {'mode':'fFire'      , 'param':'mean' , 'ymin':  0.0  , 'ymax':    10.0  , 'cbar' : 'hot_r'       },
    {'mode':'fFire'      , 'param':'std'  , 'ymin':  0.0  , 'ymax':    10.0  , 'cbar' : 'hot_r'       },
    {'mode':'fFire'      , 'param':'trend', 'ymin': -0.1  , 'ymax':     0.1  , 'cbar' : 'RdBu_r'      },
]

# -- 4.3: Settings for difference plot:
# -- Colorbar settings for data over 'Global', 'Tropics', 'Other' regions
clb_diff_limits_GTO = [
    # Fire datasets
    {'mode':'burned_area', 'param':'mean' , 'ymin': -0.001, 'ymax':    0.001 , 'cbar' : 'RdBu_r'},
    {'mode':'burned_area', 'param':'std'  , 'ymin': -0.03 , 'ymax':     0.03 , 'cbar' : 'RdBu_r'},
    {'mode':'burned_area', 'param':'trend', 'ymin': -1e-4 , 'ymax':     1e-4 , 'cbar' : 'bwr'   },
    # Carbon in vegetation
    {'mode':'cVeg'       , 'param':'mean' , 'ymin': -1.0  , 'ymax':     1.0  , 'cbar' : 'PiYG'  },
    {'mode':'cVeg'       , 'param':'std'  , 'ymin': -0.6  , 'ymax':     0.6  , 'cbar' : 'PiYG'  },
    {'mode':'cVeg'       , 'param':'trend', 'ymin': -1e-3 , 'ymax':     1e-3 , 'cbar' : 'PiYG'  },
    # Gross Primary Production
    {'mode': 'gpp'       , 'param':'mean' , 'ymin':-40.0  , 'ymax':    40.0  , 'cbar' : 'PiYG'  },
    {'mode': 'gpp'       , 'param':'std'  , 'ymin':-20.0  , 'ymax':    20.0  , 'cbar' : 'PiYG'  },
    {'mode': 'gpp'       , 'param':'trend', 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    # Net primary production
    {'mode': 'npp'       , 'param':'mean' , 'ymin':-20.0  , 'ymax':    20.0  , 'cbar' : 'PiYG'  },
    {'mode': 'npp'       , 'param':'std'  , 'ymin':-15.0  , 'ymax':    15.0  , 'cbar' : 'PiYG'  },
    {'mode': 'npp'       , 'param':'trend', 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    # Leaf Area Index
    {'mode': 'lai'       , 'param':'mean' , 'ymin': -1.0  , 'ymax':     1.0  , 'cbar' : 'PiYG'  },
    {'mode': 'lai'       , 'param':'std'  , 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    {'mode': 'lai'       , 'param':'trend', 'ymin': -1e-3 , 'ymax':     1e-3 , 'cbar' : 'PiYG'  },
    # Net Ecosystem Exchange
    {'mode': 'nee'       , 'param':'mean' , 'ymin': -30.0 , 'ymax':    30.0  , 'cbar' : 'PiYG'  },
    {'mode': 'nee'       , 'param':'std'  , 'ymin': -30.0 , 'ymax':    30.0  , 'cbar' : 'PiYG'  },
    {'mode': 'nee'       , 'param':'trend', 'ymin':  -0.5 , 'ymax':     0.5  , 'cbar' : 'PiYG'  },
    # Net Biome Production
    {'mode': 'nbp'       , 'param':'mean' , 'ymin': -30.0 , 'ymax':    30.0  , 'cbar' : 'PiYG'  },
    {'mode': 'nbp'       , 'param':'std'  , 'ymin': -30.0 , 'ymax':    30.0  , 'cbar' : 'PiYG'  },
    {'mode': 'nbp'       , 'param':'trend', 'ymin':  -0.4 , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    # CO2 Flux to Atmosphere from Fire
    {'mode':'fFire'      , 'param':'mean' , 'ymin':-10.0  , 'ymax':    10.0  , 'cbar' : 'PiYG'  },
    {'mode':'fFire'      , 'param':'std'  , 'ymin': -6.0  , 'ymax':     6.0  , 'cbar' : 'PiYG'  },
    {'mode':'fFire'      , 'param':'trend', 'ymin': -0.2  , 'ymax':     0.2  , 'cbar' : 'PiYG'  },
]

# -- Colorbar settings for data over 'Europe', 'NH' regions
clb_diff_limits_EN = [
    # Fire datasets
    {'mode':'burned_area', 'param':'mean' , 'ymin': -0.05 , 'ymax':     0.05 , 'cbar' : 'RdBu_r'},
    {'mode':'burned_area', 'param':'std'  , 'ymin': -0.03 , 'ymax':     0.03 , 'cbar' : 'RdBu_r'},
    {'mode':'burned_area', 'param':'trend', 'ymin': -1e-3 , 'ymax':     1e-3 , 'cbar' : 'bwr'   },
    # Carbon in vegetation
    {'mode':'cVeg'       , 'param':'mean' , 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    {'mode':'cVeg'       , 'param':'std'  , 'ymin': -0.2  , 'ymax':     0.2  , 'cbar' : 'PiYG'  },
    {'mode':'cVeg'       , 'param':'trend', 'ymin': -1e-3 , 'ymax':     1e-3 , 'cbar' : 'PiYG'  },     
    # Gross Primary Production
    {'mode': 'gpp'       , 'param':'mean' , 'ymin':-40.0  , 'ymax':    40.0  , 'cbar' : 'PiYG'  },
    {'mode': 'gpp'       , 'param':'std'  , 'ymin':-20.0  , 'ymax':    20.0  , 'cbar' : 'PiYG'  },
    {'mode': 'gpp'       , 'param':'trend', 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    # Net primary production
    {'mode': 'npp'       , 'param':'mean' , 'ymin':-20.0  , 'ymax':    20.0  , 'cbar' : 'PiYG'  },
    {'mode': 'npp'       , 'param':'std'  , 'ymin':-15.0  , 'ymax':    15.0  , 'cbar' : 'PiYG'  },
    {'mode': 'npp'       , 'param':'trend', 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    # Leaf Area Index
    {'mode': 'lai'       , 'param':'mean' , 'ymin': -2.0  , 'ymax':     2.0  , 'cbar' : 'PiYG'  },
    {'mode': 'lai'       , 'param':'std'  , 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    {'mode': 'lai'       , 'param':'trend', 'ymin': -1e-2 , 'ymax':     1e-2 , 'cbar' : 'PiYG'  },
    # Net Ecosystem Exchange
    {'mode': 'nee'       , 'param':'mean' , 'ymin': -7.5  , 'ymax':     7.5  , 'cbar' : 'PiYG'  },
    {'mode': 'nee'       , 'param':'std'  , 'ymin': -7.5  , 'ymax':     7.5  , 'cbar' : 'PiYG'  },
    {'mode': 'nee'       , 'param':'trend', 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    # Net Biome Production
    {'mode': 'nbp'       , 'param':'mean' , 'ymin': -7.5  , 'ymax':     7.5  , 'cbar' : 'PiYG'  },
    {'mode': 'nbp'       , 'param':'std'  , 'ymin': -7.5  , 'ymax':     7.5  , 'cbar' : 'PiYG'  },
    {'mode': 'nbp'       , 'param':'trend', 'ymin': -0.4  , 'ymax':     0.4  , 'cbar' : 'PiYG'  },
    # CO2 Flux to Atmosphere from Fire
    {'mode':'fFire'      , 'param':'mean' , 'ymin': -4.0  , 'ymax':     4.0  , 'cbar' : 'PiYG'  },
    {'mode':'fFire'      , 'param':'std'  , 'ymin': -2.0  , 'ymax':     2.0  , 'cbar' : 'PiYG'  },
    {'mode':'fFire'      , 'param':'trend', 'ymin': -0.1  , 'ymax':     0.1  , 'cbar' : 'PiYG'  },
]

# -- 4.4: Settings for plots on model grid:
clb_limits = {
        'Global' : clb_limits_GTO, # global region
        'Europe' : clb_limits_EN , # europe region
        'Tropics': clb_limits_GTO, # Tropics region --> not tested
        'NH'     : clb_limits_EN , # NH region      --> not tested 
        'Other'  : clb_limits_GTO, # other regions       
}

# -- 4.5: Settings for plots on model grid:
clb_diff_limits = {
        'Global' : clb_diff_limits_GTO, # global region
        'Europe' : clb_diff_limits_EN , # europe region
        'Tropics': clb_diff_limits_GTO, # Tropics region --> not tested
        'NH'     : clb_diff_limits_EN , # NH region      --> not tested
        'Other'  : clb_diff_limits_GTO, # other regions
}


# Section 5: Settings for subplots
# ======================================================================

# -- 5.1: Special settings for subplots positions
'''
User Settings for positions of subplots in the figure depending on projection
     This parameters are using in function collage_plot from vis_module

     NBC - I used this abbreviation for this phrase
     --> number of columns in one row
'''
# 5.1.1: Settings for 2D plot
# -- Region ---> Global. Type projection ---> 'moll' 
layout_settings_moll =  {
#  NBC    pad   w_pad   h_pad     fig length   fig hight
    1 : [ 5.0,   1.5 ,     2.5,      14.0,      12.0],
    2 : [ 5.0,   4.5 ,     4.5,      10.0,      12.0],
    3 : [ 5.0,   0.5 ,     6.5,      14.0,      12.0],
    4 : [ 5.0,   0.05,     3.5,      14.0,      10.0],
    5 : [ 5.0,   0.05,     5.5,      14.0,       9.0],
    6 : [ 5.0,   0.04,     2.5,      16.0,       8.0],
    7 : [ 5.0,   0.03,     2.5,      16.0,       7.0],
    8 : [ 5.0,   0.02,     1.5,      16.0,       6.0],
}

# Region ---> Europe, Other. Type projection ---> 'merc' 
layout_settings_merc =  {
#  NBC    pad   w_pad   h_pad     fig length   fig hight
    1 : [ 4.0,   5.0 ,     0.5,       6.0,      10.0],
    2 : [ 4.0,   5.0 ,     0.5,       8.0,      12.0],
    3 : [ 4.0,   4.0 ,     0.4,      12.0,      12.0],
    4 : [ 4.0,   2.5 ,     0.3,      14.0,      12.0],
    5 : [ 4.0,   0.5 ,     0.2,      14.0,      12.0],
    6 : [ 4.0,   0.2 ,     0.2,      14.0,      10.0],
    7 : [ 4.0,   0.2 ,     0.2,      15.0,       9.0],
    8 : [ 4.0,   0.2 ,     0.2,      16.0,       8.0],
}

# Region ---> Tropics, NH. Type projection ---> 'cyl'
layout_settings_cyl  =  {
#  NBC    pad   w_pad   h_pad     fig length   fig hight
    1 : [ 4.0,   5.0 ,     0.5,      14.0,      12.0],
    2 : [ 4.0,   5.0 ,     0.5,      14.0,      12.0],
    3 : [ 4.0,   0.5 ,     4.5,      14.0,      10.0],
    4 : [ 4.0,   0.35,     3.0,      14.0,       9.0],
    5 : [ 4.0,   0.25,     3.0,      14.0,       8.0],
    6 : [ 4.0,   0.10,     2.0,      16.0,       7.0],
    7 : [ 4.0,   0.05,     0.4,      16.0,       6.0],
    8 : [ 4.0,   0.05 ,    0.2,      16.0,       6.0],
}

# settings for tight_layout
layout_settings = {
        'Global' : layout_settings_moll, # global region
        'Europe' : layout_settings_merc, # europe region
        'Tropics': layout_settings_cyl , # Tropics region --> not tested
        'NH'     : layout_settings_cyl , # NH region      --> not tested 
        'Other'  : layout_settings_merc, # other regions       
}
# ===========================================================================
