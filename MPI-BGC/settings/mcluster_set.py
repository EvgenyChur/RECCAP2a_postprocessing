# -*- coding: utf-8 -*-
"""
Special library for the cluster machine with actual inforamtation about
location of dataset and OCN simulations. These parameters presented into
two subrotunes:

    1. datasets_catalog() - datasets for comparison
        a. mode    - type of data presented in dataset (fire, npp, gpp .... )
        b. dataset - name of dataset (you will use this name for definition of it)
        c. path    - path to the dataset
    2. ocn_catalog - OCN simulations 

Also, library has information in the dictionary - dataset_units from NetCDF
files such as: 
    1. mode          - type of data presented in dataset (fire, npp, gpp .... )
    2. short_name    - short name of the research parameter (part of y axis label)
    3. axis_name     - long name of the research parameter (part of plot titles)
    4. units_initial - original units of OCN simulations from NetCDF (not used) 
    5. units4line    - units after convertation (use it for line plots)
    6. units4collage - units after convertation (use it for collage and 2d plots)
    7. ocn_param     - name of the research patameter in OCN simulation 
    8. other param   - name of the research parameter in datasets. For example:
                       (modis_param, avhrr_param, gfed_param)

P.S.: If you want to add new datasets for comparison you have to do next steps:
    a. add you new research dataset to catalog from subrotine dataset_catalog or
       add you new OCN simulation to catalog from subroutine ocn_catalog. 
    
    b. add actual parameter to dataset_units dictionary (by analogy with fire
                                                         datasets)

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-07-07 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-08-16 Evgenii Churiulin, MPI-BGC
           Added new datasets (LAI)
    1.3    2022-09-22 Evgenii Churiulin, MPI-BGC
           Added new OCN datasets (S0 and S2Prog) + corrected ocn paths
    1.4    2023-02-13 Evgenii Churiulin, MPI-BGC
           1. Added new parameter 'attribute' into "dataset_catalog" function.
              Now, you have to write actual NetCDF attribute here.
           2. Added new parameter 'attribute_catalog' into "ocn_catalog:
              function. You have to add your OCN netcdf attribute here
           3. Deleted NetCDF attributes from "dataset_units" function. 
           4. Created new function "output_folders" for output paths
    1.5    2023-03-13 Evgenii Churiulin, MPI-BGC
           Added new function for ORCHIDEE data
    1.6    2023-05-08 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ===================

# ========================   Personal functions   ========================
# 1. datasets_catalog --> Get actual information about input datasets:
def datasets_catalog(
        # Input variables:
        # OUTPUT variables:
    )-> list[dict]:                         # Actual parameters for comparison datasets
    # -- Start program:
    # -- Main settings (common path and user)
    main = '../'                                                                # This path was changed because of security reasons
    user = 'evchur'
    # -- Subfolder settings:
    scratch = f'{main}/scratch/{user}'
    people  = f'{main}/people/{user}'
    work_1  = f'{main}/work_1/RECCAP2/EOData'
    # -- Input paths:
    catalog = [
        # Fire datasets:
        # Groups of ESA-CCL MODISv5.1 datasets:
        {'mode'      : 'burned_area',                                                              # dataset type
         'dataset'   : 'BA_MODIS',                                                                 # dataset name
         'path'      : work_1 + (
                       '/ESA-CCI/Fire_BA/ESACCI-L4_FIRE-BA-MODIS-fv5.1_2001-2018_annual.nc'),      # dataset path
         'attribute' : 'burned_area',                                                              # dataset research attribute
        },
        # (burned area = 15 PFT -> crops were deleted):
        {'mode'      : 'burned_area_nat',
         'dataset'   : 'BA_MODIS',
         'path'      : scratch + (
                       '/RESULTS/ESACCI-L4_FIRE-BA-MODIS-fv5.1_2001-2018_annual_nat.nc'),
         'attribute' : 'burned_area',
        },
        # Using in prep_ESA (burned area = 15 PFT -> crops were deleted):
        {'mode'      : 'burned_area_year',
         'dataset'   : 'BA_MODIS',
         'path'      : scratch + (
                       '/ESA_DATA/FIRE/DATA/ESACCI-L4_FIRE-BA-MODIS-fv5.1'),
         'attribute' : 'burned_area',
        },
        # Using in check_ESA_tbaf (burned area = 15 PFT -> crops were deleted) - 360*720:
        {'mode'      : 'burned_area_post',
         'dataset'   : 'BA_MODIS',
         'path'      : scratch + '/ESA_DATA/FIRE/DATA_PFT/DATA_IN/ba_fraction',
         'attribute' : 'burned_area',
        },
        # Group of ESA-CCL AVHRR_LTDR datasets:
        {'mode'      : 'burned_area',
         'dataset'   : 'BA_AVHRR',
         'path'      : scratch + (
                       '/ESACCI-L4_FIRE-BA-AVHRR-LTDR-fv1.1_1982-2018_annual.nc'),
         'attribute' : 'burned_area',
        },
        # Group of GFED datasets:
        {'mode'      : 'burned_area',
         'dataset'   : 'GFED4.1s',
         'path'      : work_1 + '/GFED4s/GFED4.1s_annual_burned_area_1997-2017.nc',
         'attribute' : 'burned_fraction',
        },

        {'mode'      : 'burned_area',
         'dataset'   : 'GFED_TOT',
         'path'      : scratch + (
                       '/GFED/GFED_annual_burned_area_2002-2020_025d.nc'),
         'attribute' : 'burned_area',
        },

        {'mode'      : 'burned_area',
         'dataset'   : 'GFED_FL',
         'path'      : scratch + (
                       '/GFED/GFED_annual_FL_burned_area_2002-2020_025d.nc'),
         'attribute' : 'burned_area'
        },
        # JULES datasets:
        {'mode'      : 'burned_area',
         'dataset'   : 'JULES',
         'path'      : main + (
                       '/work_1/RECCAP2/RECCAP2A/JULES/orig/JULES_S2Prog_burntArea.nc'),

         'attribute' : 'burnedArea'#'burntArea',
        },
        # Biomass and Cardon datasets:
        {'mode'      : 'cVeg',
         'dataset'   : '',
         'path'      : 'no_data.nc',
         'attribute' : 'no_data', 
        },
        # GPP datasets and simulations:
        {'mode'      : 'gpp',
         'dataset'   : 'MOD17A2HGFv061',
         'path'      : scratch + '/MODIS/GPP/MODIS_GPP_2000-2021.nc',
         'attribute' : 'Gpp',
        },

        {'mode'      : 'gpp',
         'dataset'   : 'MOD17A3HGFv061',
         'path'      : scratch + '/MODIS/GPP/MODIS_GPP_2000-2021.nc',
         'attribute' : 'Gpp',
        },
        # NPP datasets and simulations:
        {'mode'      : 'npp',
         'dataset'   : 'MOD17A3HGFv061',
         'path'      : scratch + '/MODIS/NPP/MODIS_NPP_2000-2021.nc',
         'attribute' : 'Npp',
         },
        # LAI datasets and simulations:
        {'mode'      : 'lai',
         'dataset'   : 'LAI_LTDR',
         'path'      : scratch + '/LAI/LTDR_LAI.720.300.1981_2020_annual.nc',
         'attribute' : 'lai',
        },

        {'mode'      : 'lai',
         'dataset'   : 'LAI_MODIS',
         'path'      : scratch + '/LAI/MODIS_LAI.720.300.2000_2020.nc',
         'attribute' : 'lai',
        },

        {'mode'      : 'lai',
         'dataset'   : 'GLOBMAP',
         'path'      : scratch + '/LAI/GLOBMAP_LAI.720.300.1982_2020.nc',
         'attribute' : 'lai',
        },
        # NEE datasets and simulations:
        {'mode'      : 'nee',
         'dataset'   : '',
         'path'      : 'no_data.nc',
         'attribute' : 'no_data',
        },
        # NBP datasets and simulations:
        {'mode'      : 'nbp',
         'dataset'   : '',
         'path'      : 'no_data.nc',
         'attribute' : 'no_data',
        },
        # fFire datasets and simulations:
        {'mode'      : 'fFire',
         'dataset'   : 'GFED4.1s',
         'path'      : work_1 + (
                       '/GFED4s/GFED4.1s_annual_emissions_1997-2020.nc'),
         'attribute' : 'C'
        },
        # GFED - Total biomass burning carbon emissions from aboveground
        {'mode'      : 'fFire',
         'dataset'   : 'GFED_AG_TOT',
         'path'      : scratch + (
                       '/GFED/GFED_annual_C_AG_TOT_2002-2020_025d.nc'),
         'attribute' : 'c_ag_tot'
        },
        # GFED - Total biomass burning carbon emissions from belowground
        {'mode'      : 'fFire',
         'dataset'   : 'GFED_BG_TOT',
         'path'      : scratch + (
                       '/GFED/GFED_annual_C_BG_TOT_2002-2020_025d.nc'),
         'attribute' : 'c_bg_tot'
        },
        # GFED - Fire-related forest loss carbon emissions from aboveground
        {'mode'      : 'fFire',
         'dataset'   : 'GFED_AG_FL',
         'path'      : scratch + (
                       '/GFED/GFED_annual_C_AG_FL_2002-2020_025d.nc'),
         'attribute' : 'c_ag_fl'
        },
        # GFED - Fire-related forest loss carbon emissions from belowground
        {'mode'      : 'fFire',
         'dataset'   : 'GFED_BG_FL',
         'path'      : scratch + (
                       '/GFED/GFED_annual_C_BG_FL_2002-2020_025d.nc'),
         'attribute' : 'c_bg_fl'
        },
        # Land Cover Fraction:
        {'mode'      : 'landCoverFrac',
         'dataset'   : '',
         'path'      : 'no_data.nc',
         'attribute' : 'no_data',
        },
        # NDEP - OCN input field
        {'mode'      : 'ndep',
         'dataset'   : 'NDEP',
         'path'      : scratch + '/ESA_DATA/FIRE/DATA_NDEP/ndep_2018.nc',
         'attribute' : 'ndep',
         },
        # LANDCOVER - OCN input data
        {'mode'      : 'landuse_2010',
         'dataset'   : 'LANDCOVER',
         'path'      : main + (
                      '/work_1/RECCAP2/RECCAP_ESACCI/OCNForcing/'
                      'LANDUSE/GH_GCP2021/land-use_2010.nc'),
         'attribute' : 'landCoverFrac',
        },
    ]
    return catalog
# ----------------------------------------------------------------------

# 2. ocn_catalog --> Get actual input information about OCN simulations:
def ocn_catalog(
        # Input variables:
        var:str,                           # Reseacrh parameter: (burned_area, npp, gpp, ...)
        # OUTPUT variables:
    ) -> tuple[dict,                       # Input paths for OCN simulations (catalog)
               dict]:                      # NetCDF atribitte for OCN simulation (attribute_catalog)
    # -- Start program:
    if var == 'burned_area':
        var = 'burnedArea'
    print('mcluster', var)
    # -- Common path for all OCN simulations:
    pin = '../work_1/RECCAP2/RECCAP2A'                                          # This path was changed because of security reasons
    # -- Input paths:
    catalog = (
        {# OCN simulations with fire
         'OCN_S2.1'    : pin + f'/NRT/OCNout/Fire/OCN_S2.1_{var}.nc',
         'OCN_S3.1'    : pin + f'/NRT/OCNout/Fire/OCN_S3.1_{var}.nc',
         'OCN_S2.2'    : pin + f'/NRT/v2022/OCNfire/OCN_S2.2_{var}.nc',
         'OCN_S3.2'    : pin + f'/NRT/v2022/OCNfire/OCN_S3.2_{var}.nc',
         'OCN_S2.1.1'  : pin + f'/NRT/v2022.3/OCN_S2.1.1_{var}.nc',
         # OCN simulations without fire
         'OCN_S2.1_nf' : pin + f'/NRT/OCNout/NoFire/OCN_S2.1_{var}.nc',
         'OCN_S3.1_nf' : pin + f'/NRT/OCNout/NoFire/OCN_S3.1_{var}.nc',
         # OCN simulation (v2022_10)
         'OCN_S0'      : pin + f'/OCN/OCN_S0_{var}.nc',
         'OCN_S2Prog'  : pin + f'/OCN/OCN_S2Prog_{var}.nc',
         'OCN_S2Diag'  : pin + f'/OCN/OCN_S2Diag_{var}.nc',
         # OCN simulation (v2023_02)
         'OCN_Spost_v3'  : pin + f'/v202302/OCN/Spost_1850-2020/OCN_Spost_v3_{var}.nc',
         'OCN_S0_v3'     : pin + f'/v202302/OCN/S0_1960-2020/OCN_S0_{var}.nc',
         'OCN_S2Prog_v3' : pin + f'/v202302/OCN/S2Prog_1960-2022/OCN_S2Prog_{var}.nc',
         'OCN_S2Diag_v3' : pin + f'/v202302/OCN/S2Diag_2003-2020/OCN_S2Diag_{var}.nc',
        }
    )
    # -- OCN NetCDF attributes:
    attribute_catalog = {
         'burned_area'   : 'burnedArea',
         'cVeg'          : 'cVeg',
         'npp'           : 'npp',
         'gpp'           : 'gpp',
         'fFire'         : 'fFire',
         'nee'           : 'nee',
         'lai'           : 'lai',   
         'nbp'           : 'nbp',
         'landCoverFrac' : 'landCoverFrac',
    }
    return catalog, attribute_catalog   
# ----------------------------------------------------------------------

# 3. jules_catalog --> Get actual input information about JULES simulations:
def jules_catalog(
        # Input variables:
        var:str,                           # Reseacrh parameter: (burned_area, npp, gpp, ...)
        # OUTPUT variables:
    ) -> tuple[dict,                       # Input paths for JULES simulations (catalog)
               dict]:                      # NetCDF atribitte for JULES simulation (attribute_catalog)
    # -- Start program:
    # Common path for all OCN simulations
    #pin = '../work_1/RECCAP2/RECCAP2A'                                         # This path was changed because of security reasons
    pin = '../scratch/evchur/JULES/DATA'                                        # This path was changed because of security reasons

    if var == 'burned_area':
        var = 'burntArea'
    # -- Input paths:
    catalog = (
        {# Old versions of JULES simulation:
         'JUL_S2Prog_v301122' : pin + f'/JULES/orig/JULES_S2Prog_{var}.nc',
         'JUL_S2Diag_v301122' : pin + f'/JULES/orig/JULES_S2Diag_{var}.nc',
         # New version of JULES simulation:
         'JUL_S2Prog'         : pin + f'/JULES_S2Prog_{var}_mod.nc',
         'JUL_S2Diag'         : pin + f'/JULES_S2Diag_{var}_mod.nc',
         #'JUL_S2Prog'         : pin + f'/v202302/JULES/Prog/JULES_S2_v6.3_{var}.nc',
         #'JUL_S2Diag'         : pin + f'/v202302/JULES/Diag/JULES_S2_v6.3_{var}.nc',
         }
    )
    # -- There is no NEE data from JULES simulations:
    attribute_catalog = {
        # Scrip param    NetCDF param      Units
         'burned_area' : 'burntArea',    # %
         'cVeg'        : 'cVeg',         # kg C m-2
         'npp'         : 'npp',          # kg C m-2 s-1
         'gpp'         : 'gpp',          # kg C m-2 s-1
         'fFire'       : 'fFire',        # kg C m-2 s-1
         'lai'         : 'lai',          # 1
         'nbp'         : 'nbp',          # kg C m-2 s-1
    }
    return  catalog, attribute_catalog
# ----------------------------------------------------------------------

# 4. orchidee_catalog --> Get actual input information about ORCHIDEE simulations:
def orchidee_catalog(
        # Input variables:
        var:str,                           # Reseacrh parameter: (burned_area, npp, gpp, ...)
        # OUTPUT variables:
    ) -> tuple[dict,                       # Input paths for OCN simulations (catalog)
               dict]:                      # NetCDF atribitte for OCN simulation (attribute_catalog)
    # -- Start program:
    # Common path for all OCN simulations
    pin = '../scratch/evchur/ORCHIDEE-MICT/OCN_grid'                            # This path was changed because of security reasons

    if var == 'burned_area':
        #var = 'burnedArea'
        var = 'burntArea'
    # -- Input paths:
    catalog = (
        {
         'ORC_S0'     : pin + f'/ORCHIDEE_S0_{var}_tmp.nc',
         'ORC_S2Prog' : pin + f'/ORCHIDEE_S2Prog_{var}_tmp.nc',
         'ORC_S2Diag' : pin + f'/ORCHIDEE_S2Diag_{var}_tmp.nc',
        }
    )
    # -- There is no NEE and NPP data from ORCHIDEE simulations
    attribute_catalog = {
        # Scrip param    NetCDF param     Units
         'burned_area'   : 'burntArea',  # %
         'cVeg'          : 'cVeg',       # kg C m-2
         'gpp'           : 'gpp',        # kg C m-2 s-1
         'fFire'         : 'fFire',      # kg C m-2 s-1
         'lai'           : 'lai',        # m2 m-2
         'nbp'           : 'nbp',        # kg C m-2 s-1
    }
    return  catalog, attribute_catalog
# ----------------------------------------------------------------------

# 5. dataset_units --> Get actual auxiliary (shorh and full dataset names,
#                      dataset units) information for plots:
def dataset_units(
        # Input variables:
        # OUTPUT variables:
    ) -> list[dict]:                   # Output parameters for plots
    # -- Define output parameters:
    dataset_info = [
        # # Fire datasets and simulations:
        {'mode'          : 'burned_area',      # mode for work
         'short_name'    : 'BA',               # short name for y axis
         'axis_name'     : 'Burned area',      # parameter name
         'units_initial' : 'fraction (0 - 1)', # initial units in OCN simulations
         'units4line'    : '1000 km\u00B2',    # units for linear plot  (total)
         'units4collage' : '1000 km\u00B2',    # units for collage plot (2d maps)
        },
        # Biomass and Cardon (cVeg) datasets:
        {'mode'          : 'cVeg',
         'short_name'    : 'cVeg',
         'axis_name'     : 'Carbon in Vegetation',
         'units_initial' : 'kg C m^-2',
         'units4line'    : 'Pg C',
         'units4collage' : 'kgC m \u207b\u00B2',
        },
        # Net primary production (NPP) datasets and simulations:
        {'mode'          : 'npp',
         'short_name'    : 'NPP',
         'axis_name'     : 'Net Primary Production',
         'units_initial' : 'kg C m^-2 s^-1',
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # Gross primary production (GPP) datasets and simulations:
        {'mode'          : 'gpp',
         'short_name'    : 'GPP',
         'axis_name'     : 'Gross Primary Production',
         'units_initial' : 'kg C m^-2 s^-1',
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # Leaf area index (LAI) datasets and simulations:
        {'mode'          : 'lai',
         'short_name'    : 'LAI',
         'axis_name'     : 'Leaf Area Index',
         'units_initial' : 'm^2 m^-2 or --',
         'units4line'    : 'm\u00B2 m\u207b\u00B2',
         'units4collage' : 'm\u00B2 m\u207b\u00B2',
        },
        # Carbon emission (fFire) datasets and simulations:
        {'mode'          : 'fFire',
         'short_name'    : 'fFire',
         'axis_name'     : 'CO2 Flux to Atmosphere from fire',
         'units_initial' : 'kg C m^-2 s^-1',
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # Net Ecosystem Exchange (NEE) datasets and simulations:
        {'mode'          : 'nee',
         'short_name'    : 'NEE',
         'axis_name'     : 'Net Ecosystem Exchange',
         'units_initial' : 'kg C m^-2 s^-1',
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # -- Net Biome Production (NBP) datasets and simulations:
        {'mode'          : 'nbp',
         'short_name'    : 'NBP',
         'axis_name'     : 'Net Biome Production',
         'units_initial' : 'kg C m^-2 s^-1',
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # -- Land cover fraction data:
        {'mode'          : 'landCoverFrac',
         'short_name'    : 'landCoverFrac',
         'axis_name'     : 'Land Cover Fraction',
         'units_initial' : '% of gridcell',
         'units4line'    : ' -- ',
         'units4collage' : ' -- ',
        },
        # -- NDEP data:
        {'mode'          : 'ndep',
         'short_name'    : 'ndep',
         'axis_name'     : 'ndep',
         'units_initial' : ' -- ',
         'units4line'    : ' -- ',
         'units4collage' : ' -- ',
        },
    ]
    return dataset_info
# ----------------------------------------------------------------------

# 6. output_folders --> Get actual output paths for calculation results
def output_folders(
        # Input variables:
        # OUTPUT variables:
    ) -> dict:                                  # Output paths
    # -- Start function:
    user = 'evchur'

    # 1. Path settings for cluster:
    # -- Common path (all scripts):
    main = '../'                                                                # This path was changed because of security reasons
    # -- Output path common for main scripts:
    main_pout = main + f'/scratch/{user}/RESULTS'
    # -- Output path common for data in RECCAP2:
    reccap2   = main + '/work_1/RECCAP2'
    # -- Output path for preprocessing:
    prep_dat  = main + f'/scratch/{user}/ESA_DATA/FIRE/DATA_PFT'
    # -- Output path common for test scripts (test figures and data):
    test_fig  = main + f'/scratch/{user}/RESULTS/TESTS/FIGURES'
    test_dat  = main + f'/scratch/{user}/RESULTS/TESTS/DATA'

    # -- Unic folders for output results:
    pouts = {
        # Script name               Output data path
        # 1. Folder --> libraries scripts
        'lib4upscaling_support' : test_fig  + '/UPSCAL',
        # 2. Folder --> main scripts
        'ba_esa_pft'            : main_pout + '/ESA_PFT',
        'ba_ocn_pft'            : main_pout + '/OCN_PFT',
        'check_ESA_tbaf'        : main_pout + '/DIFF_TBAF',
        'check_ocn_pft'         : main_pout + '/PFT_COMP',
        'fire_ratio'            : main_pout + '/FIRE_RATIO',
        'fire_xarray'           : main_pout,
        'landcover'             : main_pout + '/DIFF_BA_by_PFT',
        'mpost4burn_area_OCN'   : reccap2   + '/RECCAP2A/v202302/OCN/',
        'mpost4burn_area_MODIS' : main_pout,
        # 3. Folder --> preprocessing scripts
        'prep_ESA_data'         : prep_dat  + '/DATA_IN',
        'prep_ESA_fig'          : test_fig  + '/PREP_ESA',
        # 4. Folder --> Test scripts
        '2dmap4sites'           : test_fig  + '/2D_MAP',
        'ctr_alg4ocn'           : 'There are no output files',
        'ctr_interpolation'     : 'There are no output files',
        'ctr4ocn_out'           : 'UPDATing LATER',
        'fast_test'             : test_fig  + '/FAST_TEST',
        'ffire_test'            : test_fig  + '/fFIRE_TEST',
        'lpjFire_coef'          : test_fig  + '/LPG_COEF',
        'ocn_data4ctr_alg'      : 'There are no output files',
        'OCN_param'             : test_fig  + '/OCN_PARAM',
        'rand_ts4s0'            : test_dat  + '/RUND_TS',
    }
    return pouts
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # -- User settings
    lprint = True
    nstars = 50
    var = 'fire'
    # -- Main program:
    datasets_paths = datasets_catalog(var)
    ocn_paths      = ocn_catalog()
    datasets_data  = dataset_units()
    data_out       = output_folders()
    # -- Print info:
    if lprint is True:
        print('*' * 50, '\n')
        print(datasets_paths)
        print('*' * 50, '\n')
        print(ocn_path)
        print('*' * 50, '\n')
        print(params)
        print('*' * 50, '\n')
        print(datasets_data)
        print('*' * 50, '\n')
        print(outputs)