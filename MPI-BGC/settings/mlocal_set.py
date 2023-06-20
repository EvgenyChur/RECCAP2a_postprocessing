# -*- coding: utf-8 -*-
"""
Special library for the local machine with actual inforamtation about location 
of dataset and OCN simulations. These parameters presented into two subrotunes:
    
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
    1.1    2022-07-07 Evgenii Churiulin, Max Planck Institute for Biogeochemistry
           Initial release
    1.2    2022-08-16 Evgenii Churiulin, MPI-BGC
           Added new datasets (LAI) 
    1.3    2022-09-22 Evgenii Churiulin, MPI-BGC
           Added new OCN datasets (S0 and S2Prog) + delete ocn paths 
    1.4    2023-02-13 Evgenii Churiulin, MPI-BGC
           1. Added new parameter 'attribute' into "dataset_catalog" function. Now,
              you have to write actual NetCDF attribute here.
           2. Added new parameter 'attribute_catalog' into "ocn_catalog: function.
              Now, you have to add your OCN netcdf attribute here
           3. Deleted NetCDF attributes from "dataset_units" function. 
           4. Created new function "output_folders" for output paths
    1.5    2023-05-08 Evgenii Churiulin, MPI-BGC
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
    main    = 'C:/Users/evchur/Desktop/DATA'
    catalog = [
        # Fire datasets and simulations:
        # Groups of ESA-CCL MODISv5.1 datasets-
        {'mode'      : 'burned_area',                                          # Dataset type
         'dataset'   : 'BA_MODIS',                                             # Dataset name
         'path'      : main + (
                       '/ESACCI-L4_FIRE-BA-MODIS-fv5.1_2001-2018_annual.nc'),  # Dataset path
         'attribute' : 'burned_area',                                          # Dataset research attribute
        },

        {'mode'      : 'burned_area_nat',
         'dataset'   : 'BA_MODIS',
         'path'      : main + (
                       '/ESACCI-L4_FIRE-BA-MODIS-fv5.1_2001-2018_annual_nat.nc'),
         'attribute' : 'burned_area',
        },
        # using in prep_ESA (burned area = 15 PFT -> crops were deleted)
        {'mode'      : 'burned_area_year',
         'dataset'   : 'BA_MODIS',
         'path'      : main + '/FIRE/DATA/ESACCI-L4_FIRE-BA-MODIS-fv5.1',
         'attribute' : 'burned_area',
        },
        # Using in check_ESA_tbaf (burned area = 15 PFT -> crops were deleted) - 360*720
        {'mode'      : 'burned_area_post',
         'dataset'   : 'BA_MODIS',
         'path'      : main + '/FIRE/DATA_PFT/ba_fraction',
         'attribute' : 'burned_area',
        },
        # Group of ESA-CCL AVHRR_LTDR datasets
        {'mode'      : 'burned_area',
         'dataset'   : 'BA_AVHRR',
         'path'      : main + (
                       '/ESACCI-L4_FIRE-BA-AVHRR-LTDR-fv1.1_1982-2018_annual.nc'),
         'attribute' : 'burned_area',
        },
        # Group of GFED datasets
        {'mode'      : 'burned_area',
         'dataset'   : 'GFED4.1s',
         'path'      : main + '/GFED4.1s_annual_burned_area_1997-2017.nc',
         'attribute' : 'burned_fraction',
        }, 

        {'mode'      : 'burned_area',
         'dataset'   : 'GFED_TOT',
         'path'      : main + (
                       '/GFED/GFED_annual_burned_area_2002-2020_025d.nc'),
         'attribute' : 'burned_area',
        },

        {'mode'      : 'burned_area',
         'dataset'   : 'GFED_FL',
         'path'      : main + (
                       '/GFED/GFED_annual_FL_burned_area_2002-2020_025d.nc'),
         'attribute' : 'burned_area'
        },
        # JULES datasets:
        {'mode'      : 'burned_area',
         'dataset'   : 'JULES',
         'path'      : main + (
                       '/JULES_DATA/JULES_S2_v6.3_burntArea.nc'),
         'attribute' : 'burntArea',
        },
        # Biomass and Cardon datasets:
        {'mode'      : 'cVeg',
         'dataset'   : '',
         'path'      : f'{main}/no_data.nc',
         'attribute' : 'no_data',
         },
        # GPP datasets and simulations:
        {'mode'      : 'gpp',
         'dataset'   : 'MOD17A2HGFv061',
         'path'      : main + '/MODIS_GPP_2000-2021.nc',
         'attribute' : 'Gpp',
         },
        # NPP datasets and simulations:
        {'mode'      : 'npp',
         'dataset'   : 'MOD17A3HGFv061',
         'path'      : main + '/MODIS/NPP/MODIS_NPP_2000-2021.nc',
         'attribute' : 'Npp',
        },
        # LAI datasets and simulations:
        {'mode'      : 'lai',
         'dataset'   : 'LAI_LTDR',
         'path'      : main + '/LAI/LTDR_LAI.720.300.1981_2020_annual.nc',
         'attribute' : 'lai',
        }, 

        {'mode'      : 'lai',
         'dataset'   : 'LAI_MODIS',
         'path'      : main + '/LAI/MODIS_LAI.720.300.2000_2020.nc',
         'attribute' : 'lai',
        },

        {'mode'      : 'lai',
         'dataset'   : 'GLOBMAP',
         'path'      : main + '/LAI/GLOBMAP_LAI.720.300.1982_2020.nc',
         'attribute' : 'lai',
        }, 
        # NEE datasets and simulations:
        {'mode'      : 'nee',
         'dataset'   : '',
         'path'      : main + '/no_data.nc',
         'attribute' : 'no_data',
        },
        # Net Biome Production datasets and simulations:
        {'mode'      : 'nbp',
         'dataset'   : '',
         'path'      : main + '/no_data.nc',
         'attribute' : 'no_data',
        },
        # Carbon emission datasets and simulations:
        {'mode'      : 'fFire',
         'dataset'   : 'GFED4.1s',
         'path'      : main + '/GFED4.1s_annual_emissions_1997-2020.nc',
         'attribute' : 'C',
        },
        # Land Cover Fraction:
        {'mode'      : 'landCoverFrac',
         'dataset'   : '',
         'path'      : main + '/no_data.nc',
         'attribute' : 'no_data',
        },
        # NDEP - OCN input field:
        {'mode'      : 'ndep',
         'dataset'   : 'NDEP',
         'path'      : main + '/FIRE/DATA_NDEP/ndep_2018.nc',
         'attribute' : 'ndep',
        },
        # LANDCOVER - OCN input data:
        {'mode'      : 'landuse_2010',
         'dataset'   : 'LANDCOVER',
         'path'      : main + '/LANDCOVER/land-use_2010.nc',
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

    main     = 'C:/Users/evchur/Desktop/DATA'
    # In case of RECCAP project (Ana simulations) use these path:
    fin_rec  = f'{main}/OCN_fire/RECCAP_DATA/OCN'   # simulations with fire
    nfin_rec = f'{main}/OCN_nfire/RECCAP_DATA/OCN'  # simulations without fire

    # In case of the RECCAP2 data (my simulations) use these path:
    fin_rec2 = f'{main}/OCN_fire/RECCAP2_DATA'   # simulations with    fire
    # -- Input paths:
    catalog = (
        {# OCN simulations with fire (RECCAP project)
         'OCN_S2.1'    : f'{fin_rec}_S2.1_{var}.nc' ,
         'OCN_S2.2'    : f'{fin_rec}_S2.2_{var}.nc' ,
         'OCN_S3.1'    : f'{fin_rec}_S3.1_{var}.nc' ,
         'OCN_S3.2'    : f'{fin_rec}_S3.2_{var}.nc' ,
         # OCN simulations without fire (RECCAP project)
         'OCN_S2.1_nf' : f'{nfin_rec}_S2.1_{var}.nc',
         'OCN_S3.1_nf' : f'{nfin_rec}_S3.1_{var}.nc',
         # OCN simulations (RECCAP2A project)
         'OCN_S0'      : f'{fin_rec2}/OCN_S0_{var}.nc',
         'OCN_S2Prog'  : f'{fin_rec2}/OCN_S2Prog_{var}.nc',
         'OCN_S2Diag'  : f'{fin_rec2}/OCN_S2Diag_{var}.nc',
         # OCN simulations (RECCAP2A project - new cluster)
         'OCN_Spost_v3'  : fin_rec2 + f'/Spost_1850-2020/OCN_Spost_v3_{var}.nc',
         'OCN_S0_v3'     : fin_rec2 + f'/S0_1960-2020/OCN_S0_{var}.nc',
         'OCN_S2Prog_v3' : fin_rec2 + f'/S2Prog_1960-2022/OCN_S2Prog_{var}.nc' ,
         'OCN_S2Diag_v3' : fin_rec2 + f'/S2Diag_2003-2020/OCN_S2Diag_{var}.nc' ,
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
    pin = 'C:/Users/evchur/Desktop/JULES'

    if var == 'burned_area':
        var = 'burntArea'
    # -- Input paths:
    catalog = (
        {# Old versions of JULES simulation:
         'JULES_S2Prog_v301122' : pin + '/JULES/orig/JULES_S2Prog_{var}.nc',
         'JULES_S2Diag_v301122' : pin + '/JULES/orig/JULES_S2Diag_{var}.nc',
         # New version of JULES simulation:
         'JULES_S2Prog'         : pin + '/v202302/JULES/JULES_S2Prog_{var}.nc',
         'JULES_S2Diag'         : pin + '/v202302/JULES/JULES_S2Diag_{var}.nc',
         }
    )
    # -- There is no NEE data from JULES simulations:
    attribute_catalog = {
         'burned_area' : 'burntArea',  # s-1  or %
         'cVeg'        : 'cVeg',       # Kg/m-2
         'npp'         : 'npp',        # kg/m2/360days
         'gpp'         : 'gpp',        # Kg/m-2/s-1
         'fFire'       : 'fFire',      # Kg/m-2/360
         'lai'         : 'lai',        # 1
         'nbp'         : 'nbp',        # Kg/m2/360
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
    pin = 'C:/Users/evchur/Desktop/ORCHIDEE'

    if var == 'burned_area':
        #var = 'burnedArea'
        var = 'burntArea'

    catalog = (
        {
         'ORC_S0'     : pin + f'/ORCHIDEE_S0_{var}.nc',
         'ORC_S2Prog' : pin + f'/ORCHIDEE_S2Prog_{var}.nc',
         'ORC_S2Diag' : pin + f'/ORCHIDEE_S2Diag_{var}.nc',
        }
    )

    attribute_catalog = {
         'burned_area'   : 'burntArea',  # units = "%"
         'cVeg'          : 'cVeg',       # units = "kg C m-2"
         'gpp'           : 'gpp',        # units = "kg C m-2 s-1";
         'fFire'         : 'fFire',      # units = "kg C m-2 s-1"
         'lai'           : 'lai',        # units = "m2 m-2"
         'nbp'           : 'nbp',        # units = "kg C m-2 s-1"
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
        # Fire datasets and simulations:
        {'mode'         : 'burned_area',                 # mode for work
         'short_name'   : 'BA',                          # short name for y axis
         'axis_name'    : 'Burned area',                 # parameter name 
         'units_initial': 'fraction (0 - 1)',            # initial units in OCN simulations 
         'units4line'   : '1000 km\u00B2',               # units for linear plot  (total)
         'units4collage': '1000 km\u00B2',               # units for collage plot (2d maps)
        },
        # Biomass and Cardon datasets:
        {'mode'         : 'cVeg',
         'short_name'   : 'cVeg',
         'axis_name'    : 'Carbon in Vegetation',
         'units_initial': 'kg C m^-2', 
         'units4line'   : 'Pg C', 
         'units4collage': 'kgC m \u207b\u00B2',
        },
        # NPP datasets and simulations:
        {'mode'          : 'npp', 
         'short_name'    : 'NPP',
         'axis_name'     : 'Net Primary Production',
         'units_initial' : 'kg C m^-2 s^-1', 
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # GPP datasets and simulations:
        {'mode'          : 'gpp',
         'short_name'    : 'GPP',
         'axis_name'     : 'Gross Primary Production',
         'units_initial' : 'kg C m^-2 s^-1',
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # LAI datasets and simulations:
        {'mode'          : 'lai',
         'short_name'    : 'LAI',
         'axis_name'     : 'Leaf Area Index',
         'units_initial' : 'm^2 m^-2 or --',
         'units4line'    : 'm\u00B2 m\u207b\u00B2',
         'units4collage' : 'm\u00B2 m\u207b\u00B2',
        },
        # Carbon emission datasets and simulations:
        {'mode'          : 'fFire',
         'short_name'    : 'fFire',
         'axis_name'     : 'CO2 Flux to Atmosphere from fire',
         'units_initial' : 'kg C m^-2 s^-1',   
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # Net Ecosystem Exchange datasets and simulations:
        {'mode'          : 'nee',
         'short_name'    : 'NEE',
         'axis_name'     : 'Net Ecosystem Exchange',
         'units_initial' : 'kg C m^-2 s^-1', 
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # Net Biome Production datasets and simulations:
        {'mode'          : 'nbp',
         'short_name'    : 'NBP',
         'axis_name'     : 'Net Biome Production',
         'units_initial' : 'kg C m^-2 s^-1', 
         'units4line'    : 'Pg C yr\u207b\u00B9',
         'units4collage' : 'gC m\u207b\u00B2 yr\u207b\u00B9',
        },
        # Land cover fraction:
        {'mode'          : 'landCoverFrac',
         'short_name'    : 'landCoverFrac',
         'axis_name'     : 'Land Cover Fraction', 
         'units_initial' : ' % of gridcell', 
         'units4line'    : ' -- ',
         'units4collage' : ' -- ',
        },
        # NDEP:
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
    user   = 'evchur'
    
    # 1. Path settings for local machine
    # 1.1 Common path (all scripts)
    main   = f'C:/Users/{user}/RESULTS'
    # 1.2 Output path common for main scripts:
    main_pout     = main
    # 1.3 Output path common for data in RECCAP2:
    reccap2  = f'C:/Users/{user}/Desktop/DATA'
    # 1.4 Output path for preprocessing:
    prep_dat = f'C:/Users/{user}/Desktop/DATA/FIRE'
    # 1.5 Output path common for test scripts (test figures and data):
    test_fig = main + '/TESTS/FIGURES'
    test_dat = main + '/TESTS/DATA'

    # -- Unic folders for output results:
    pouts = {
        # Script name                  Output data path
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
        'mpost4burn_area_OCN'   : reccap2   + '/OCN_fire/RECCAP2_DATA',
        'mpost4burn_area_MODIS' : reccap2,
        # 3. Folder --> preprocessing scripts
        'prep_ESA_data'         : prep_dat  + '/DAPA_PFT',
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
    var = 'burned_area'
    # -- Main program:
    datasets_paths = datasets_catalog()
    ocn_path,params = ocn_catalog(var)
    datasets_data = dataset_units()
    outputs = output_folders()
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