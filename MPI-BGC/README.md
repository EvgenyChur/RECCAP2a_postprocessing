# ESA-CCI RECCAP2A

## Available datasets and model simulations (actual on 06.06.2023):
1. `ESA-CCI MODIS v5.0` - The ESA Fire Disturbance Climate Change Initiative (CCI) project has produced maps of global burned area derived from satellite observations. The MODIS Fire_cci v5.1 grid product described here contains gridded data on global burned area derived from the MODIS instrument onboard the TERRA satellite at 250m resolution for the period 2001 to 2019. This product supercedes the previously available MODIS v5.0 product. The v5.1 dataset was initially published for 2001-2017, and has been periodically extended to include 2018 to 2020. This gridded dataset has been derived from the MODIS Fire_cci v5.1 pixel product (also available) by summarising its burned area information into a regular grid covering the Earth at 0.25 x 0.25 degrees resolution and at monthly temporal resolution. Information on burned area is included in 23 individual quantities: sum of burned area, standard error, fraction of burnable area, fraction of observed area, number of patches and the burned area for 18 land cover classes, as defined by the Land_Cover_cci v2.0.7 product. For further information on the product and its format see the Fire_cci product user guide in the linked documentation. More information about dataset you can find on [the official web-page][1]. We used this dataset for several different tasks, ***all modifications of ESA-CCI MODIS v5.0 data are available by `BA_MODIS` dataset name***. We have next modifications:
    - Annual ESA-CCI MODISv5.0 burned area data. Data available from **2001 to 2018** year. To use this data you have to use parameter `burned_area` and dataset name `BA_MODIS`in *get_path_in* function;
    - Annual ESA-CCI MODISv5.0 burned area data for natural PFT. Natural means that all *cropts PFTs* were deleted from the data. Data available from **2001 to 2018** year. To use this data you have to use parameter `burned_area_nat` and dataset name `BA_MODIS` in *get_path_in* function;
    - Monthly ESA-CCI MODISv5.1 burned area data. Data available from **2001 to 2020** year. To use this data you have to use parameter `burned_area_year` and dataset name `BA_MODIS` in *get_path_in* function. I used this data for preparing intial data for running OCN model;
    - Monthly ESA-CCI MODISv5.1 burned area data for natural PFT re-interpolated to OCN grid (`360*720`). Natural means that all *cropts PFTs* were deleted from the data. Data available from **2001 to 2020** year. To use this data you have to use parameter `burned_area_post` and dataset name `BA_MODIS` in *get_path_in* function. Data were calculated based on Monthly ESA-CCI MODISv5.1 values.

<p style="text-align: center"><img src="https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/ADDITIONAL_MATERIALS/ESA_CCI_MODIS_example.jpg"></p>

**Figure 1.** Total burned area for the year 2019. Figure copied from the official dataset documentation ([Chuvieco, E., et al., 2019][1])

2. `ESA-CCI L4 AVHRR-LTDR` -  the first global burned area (BA) product derived from the land long term data record (LTDR), a long-term 0.05-degree resolution dataset generated from advanced very high resolution radiometer (AVHRR) images. Daily images were combined in monthly composites using the maximum temperature criterion to enhance the burned signal and eliminate clouds and artifacts. A synthetic BA index was created to improve the detection of the BA signal. This index included red and near infrared reflectance, surface temperature, two spectral indices, and their temporal differences. Monthly models were generated using the random forest classifier, using the twelve monthly composites of each year as the predictors. Training data were obtained from the NASA MCD64A1 collection 6 product (500 m spatial resolution) for eight years of the overlapping period (2001–2017). This included some years with low and high fire occurrence. Results were tested with the remaining eight years. Pixels classified as burned were converted to burned proportions using the MCD64A1 product. The final product (named FireCCILT10) estimated BA in 0.05-degree cells for the 1982 to 2017 period (excluding 1994, due to input data gaps). This product is the longest global BA currently available, extending almost 20 years back from the existing NASA and ESA BA products. More information about dataset you can find on [the official web-page][2]. ***This dataset is available by `BA_AVHRR` dataset name***.
    - Annual ESA-CCI L4 AVHRR-LTDR burned area data. Data available from **1982 to 2018** year. To use this data you have to use parameter `burned_area` and dataset name `BA_AVHRR` in *get_path_in* function;
    - Annual LTDR LAI data.  Data available from **1981 to 2020** year. To use this data you have to use parameter `lai` and dataset name `LAI_LTDR` in *get_path_in* function.

<p style="text-align: center"><img src="https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/ADDITIONAL_MATERIALS/AVHRR_example.jpg"></p>

**Figure 2.** Annual FireCCILT11 BA (at 0.25° resolution) for 2016 year. Figure copied from the official dataset publication ([Gonzalo, O., et al., 2021][2b])

3. `Global Fire Emissions Database, Version 4.1 (GFEDv4)` - This dataset provides global estimates of monthly burned area, monthly emissions and fractional contributions of different fire types, daily or 3-hourly fields to scale the monthly emissions to higher temporal resolutions, and data for monthly biosphere fluxes. The data are at 0.25-degree latitude by 0.25-degree longitude spatial resolution and are available from June 1995 through 2016, depending on the dataset. Emissions data are available for carbon (C), dry matter (DM), carbon dioxide (CO2), carbon monoxide (CO), methane (CH4), hydrogen (H2), nitrous oxide (N2O), nitrogen oxides (NOx), non-methane hydrocarbons (NMHC), organic carbon (OC), black carbon (BC), particulate matter less than 2.5 microns (PM2.5), total particulate matter (TPM), and sulfur dioxide (SO2) among others. These data are yearly totals by region, globally, and by fire source for each region.  More information about database you can find on [the official web-page][3]. ***This dataset is available by `GFED4.1s` dataset name***.
    - Annual GFED4.1s burned area data. Data available from **1997 to 2017** year. To use this data you have to use parameter `burned_area` and dataset name `GFED4.1s` in *get_path_in* function;
    - Annual GFED4.1s carbon emission data. Data available from **1997 to 2017** year. To use this data you have to use parameter `fFire` and dataset name `GFED4.1s` in *get_path_in* function.

<p style="text-align: center"><img src="https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/ADDITIONAL_MATERIALS/GFED4.1s_example.jpg"></p>

**Figure 3.** Annual burned area, averaged over 1997-2014. Figure copied from the official dataset ([web-page][3])

4. `Global Fire Emission Database` - the new version of GFED database based on global MODerate resolution Imaging Spectroradiometer(MODIS) data (500m) and incliding GFED4.1s data. More information about database you can find in the [manuscript][4]:
    - Annual GFED total burned area data. Data available from **2002 to 2020** year. To use this data you have to use parameter `burned_area` and dataset name `GFED_TOT` in *get_path_in* function;
    - Annual GFED fire-related forest burned area data. Data available from **2002 to 2020** year. To use this data you have to use parameter `burned_area` and dataset name `GFED_FL` in *get_path_in* function;
    - Annual GFED total biomass burning carbon emissions from aboveground data. Data available from **2002 to 2020** year. To use this data you have to use parameter `fFire` and dataset name `GFED_AG_TOT` in *get_path_in* function;
    - Annual GFED total biomass burning carbon emissions from belowground data. Data available from **2002 to 2020** year. To use this data you have to use parameter `fFire` and dataset name `GFED_BG_TOT` in *get_path_in* function;
    - Annual GFED fire-related forest loss carbon emissions from aboveground data. Data available from **2002 to 2020** year. To use this data you have to use parameter `fFire` and dataset name `GFED_AG_FL` in *get_path_in* function;
    - Annual GFED fire-related forest loss carbon emissions from belowground data. Data available from **2002 to 2020** year. To use this data you have to use parameter `fFire` and dataset name `GFED_BG_FL` in *get_path_in* function.

<p style="text-align: center"><img src="https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/ADDITIONAL_MATERIALS/GFED_example.jpg"></p>

**Figure 4.** Global annual burned area, averaged over 2002-2020. Figure copied from the official dataset publication ([D. van Wees et al., 2022][4])

5. `MOD17A2HGF v061` or *MODIS/Terra Gross Primary Productivity Gap-Filled 8-Day L4 Global 500 m SIN Grid* - is a cumulative 8-day composite of values with 500 meter (m) pixel size based on the radiation use efficiency concept that can be potentially used as inputs to data models to calculate terrestrial energy, carbon, water cycle processes, and biogeochemistry of vegetation. The Terra Moderate Resolution Imaging Spectroradiometer (MODIS) data product includes information about GPP and Net Photosynthesis (PSN). The PSN band values are the GPP less the Maintenance Respiration (MR). The data product also contains a PSN Quality Control (QC) layer. The quality layer contains quality information for both the GPP and the PSN.  More information about dataset you can find on [the official web-page][5]. ***This dataset is available by `MOD17A2HGFv061` dataset name***.
    - Monthly GPP data. Data available from **2000 to 2021** year. To use this data you have to use parameter `gpp` and dataset name `MOD17A2HGFv061` in *get_path_in* function.

6. `MOD17A3HGFv061` or *MODIS/Terra Net Primary Production Gap-Filled Yearly L4 Global 500 m SIN Grid* - product provides information about annual Gross and Net Primary Production (GPP and NPP) at 500 meter (m) pixel resolution. Annual Terra Moderate Resolution Imaging Spectroradiometer (MODIS) GPP and NPP is derived from the sum of all 8-day GPP Net Photosynthesis (PSN) products (MOD17A2H) from the given year. The PSN value is the difference of the GPP and the Maintenance Respiration (MR). More information about dataset you can find on [the official web-page][6]. ***This dataset is available by `MOD17A3HGFv061` dataset name***.
    - Monthly GPP data. Data available from **2000 to 2021** year. To use this data you have to use parameter `gpp` and dataset name `MOD17A3HGFv061` in *get_path_in* function;
    - Monthly NPP data. Data available from **2000 to 2021** year. To use this data you have to use parameter `npp` and dataset name `MOD17A3HGFv061` in *get_path_in* function.

7. `MODIS LAI`:
    - Annual LAI data. Data available from **2000 to 2020** year. To use this data you have to use parameter `lai` and dataset name `LAI_MODIS` in *get_path_in* function.

8. `GLOBMAP LAI (Version 3)` -  provides a consistent long-term global leaf area index (LAI) product (1981-2020, continuously updated) at 8km resolution on Geographic grid by quantitative fusion of Moderate Resolution Imaging Spectroradiometer (MODIS) and historical Advanced Very High Resolution Radiometer (AVHRR) data. The long-term LAI series was made up by combination of AVHRR LAI (1981–2000) and MODIS LAI (2001–). MODIS LAI series was generated from MODIS land surface reflectance data (MOD09A1 C6) based on the GLOBCARBON LAI algorithm (Deng et al., 2006). The relationships between AVHRR observations (GIMMS NDVI (Tucker et al., 2005)) and MODIS LAI were established pixel by pixel using two data series during overlapped period (2000–2006). Then the AVHRR LAI back to 1981 was estimated from historical AVHRR observations based on these pixel-level relationships. Detailed descriptions of algorithm and evaluation of the algorithm see Liu et al. (2012, JGR-B). More information about dataset you can find on [the official web-page][9]. ***This dataset is available by `GLOBMAP` dataset name***.
    - Annual LAI data. Data available from **1982 to 2020** year. To use this data you have to use parameter `lai` and dataset name `GLOBMAP` in *get_path_in* function;

10. `NDEP`:
    - Annual NDEP data. Data available for **2018** year. To use this data you have to use parameter `ndep` and dataset name `NDEP` in *get_path_in* function;

11. `LANDCOVER` :
    - Annual landcover data. Data available for **2010** year. To use this data you have to use parameter `landuse_2010` and dataset name `LANDCOVER` in *get_path_in* function;

12. `OCN` model - is a dynamic global vegetation model. OCN is a model of the coupled terrestrial carbon and nitrogen cycles ([Zaehle and Friend, 2010][12a]; [Zaehle et al., 2010, GBC][12b]), derived from the ORCHIDEE land-surface model ([Krinner et al., 2005][14a]). We have next simulations with such parameters as ***burned_area, cVeg, npp, gpp, fFire, nee lai, nbp, landCoverFrac***:
    - ***OCN_S0***  -> OCN simulation prepared based on OCN model version - *v2022_10*;
    - ***OCN_S2Prog*** -> OCN simulation prepared based on OCN model version - *v2022_10*;
    - ***OCN_S2Diag*** -> OCN simulation prepared based on OCN model version - *v2022_10*;
    - ***OCN_Spost_v3*** -> OCN simulation prepared based on OCN model version - *v2023_02*;
    - ***OCN_S0_v3*** -> OCN simulation prepared based on OCN model version - *v2023_02*;
    - ***OCN_S2Prog_v3*** -> OCN simulation prepared based on OCN model version - *v2023_02*;
    - ***OCN_S2Diag_v3*** -> OCN simulation prepared based on OCN model version - *v2023_02*;

<p style="text-align: center"><img src="https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/raw/Version_10112022/RESULTS/ADDITIONAL_MATERIALS/OCN_simulations.jpg"></p>

**Figure 4.** Description OCN simulations

Also, we have several historical versions from the RECCAP project: ***OCN_S2.1***, ***OCN_S2.2***, ***OCN_S2.1.1***, ***OCN_S2.1_nf***, ***OCN_S3.1***, ***OCN_S3.2*** and ***OCN_S3.1_nf***

13. `JULES` [model][13a] - is a community land surface model that is used both as a standalone model and as the land surface component in the Met Office Unified Model. JULES is a core component of both the Met Office's modelling infrastructure and NERC's Earth System Modelling Strategy. JULES is a major part of the UK's contribution to global model intercomparison projects (e.g. CMIP6) and is placed firmly at the cutting edge of international land surface modelling because of continual science development and improved accessibility. We have next simulations with such parameters as ***burned_area, cVeg, npp, gpp, fFire, lai, nbp***:
    - ***S2Prog (JULES_S2_v6.3)***
    - ***S2Diag (JULES_S2_v6.3)***

14. `ORCHIDEE` [model][14c] - is a global process-oriented Terrestrial Biosphere Model ([Krinner et al., 2005][14a]). It calculates carbon, water and energy fluxes between land surfaces and the atmosphere. The water and energy component computes major biophysical variables (albedo, roughness height, soil humidity) and solves the energy and hydrological balances at a half-hourly time step. The carbon module describes photosynthesis and respiration at the same temporal resolution; the slow components of the terrestrial carbon cycle (including LAI, carbon allocation in plant reservoirs, soil carbon dynamics, and litter decomposition) are calculated on a daily basis. A turnover rate is applied to biomass pools and produces litterfall. Litter is decomposed and goes into three soil organic carbon pools with different residence times (active, slow and passive) following the CENTURY model ([Parton et al., 1988][14b]) simulations.  We have next simulations with such parameters as ***burned_area, cVeg, gpp, fFire, lai, nbp***:
    - ***S0 (ORCHIDEE_S0)***
    - ***S2Prog (ORCHIDEE_S2Prog)***
    - ***S2Diag (ORCHIDEE_S2Prog)***

## How add new dataset?
If you want to add new dataset or model simulations for analysis you have to do next steps:
1. **/settings/mcluster.py** or **/settings/mlocal.py** and add you new dataset into next functions:
    - ***dataset_catalog*** -> if you want to add *new dataset* or *few model simulations* you have to add them as a new dictionary with such parameters as:
        1. `mode` - the main type of data from dataset. I used 8 different `mode` names for the main post-processing script. Names are similar with the main research parameters (e.g.: burned_area, cVeg or gpp). You can add you a new `mode` name. This is *the first key word* for searching, necessary dataset information;
        2. `dataset` - the name of dataset.  You can use all names, but I used short name without spaces for that purpose. `dataset` name is *the second key word* for searching, necessary dataset information;
        3. `path` - the datapath. You have to add information about the localtion of your dataset. If you use cluster, data can be located in *scratch*, *people*, or *work_1* folders;
        4. `attribute` - the NetCDF attribute name for your research parameter. This name can be different from `mode` or can be the same.
    - If you want to add *model simulations* for most of research parameters. You have to create a new function similar with ***ocn_catalog***, ***jules_catalog*** or ***orchidee_catalog***.
    - If you want to add additional *OCN*,*JULES*, *ORCHIDEE* research parameters. You have to add them to ***ocn_catalog***, ***jules_catalog*** or ***orchidee_catalog*** functions.
    - ***dataset_units*** -> add or check current values in *datasets_info* variable:
        1. `mode` - the main type of data from dataset. Type should have the same name as in ***dataset_catalog***;
        2. `short_name` - the short name of your research parameter;
        3. `axis_name` - the long name of your research parameter;
        4. `units_initial` - original units from dataset or model simulations. If you have different units, it will be better to convert them to the same units before data processing. Nevertheless, if you decided to use your dataset (model simulations) with different units you can add your convertation algorithm to the `get_data` function from **/libraries/lib4xarray.py** or you can use your additional function for that;
        5. `units4line` - units after work of `annual_mean` function from **/libraries/lib4xarray**. I used it for linear plots for domain (all grid points in one) and stations (selected grid point);
        6. `units4collage` - main units for work. Also, I used these units for statistical analisys and visualization of NetCDF data on 2D maps.
    - ***output_folders*** -> you have to adapt your output folders.
2. In case of *new function* (new model simulations) you have to add the running command to `get_path_in` function of **/settings/path_settings.py** module. Otherwise, you can ignore this step.
3. **/settings/user_settings.py** and add new information for the next variables:
    - `av_datasets` - available datasets (dictionary). Dictionary keys and elements have to have the same names as `mode` and `dataset`from **/settings/mcluster.py** or **/settings/mlocal.py**
    - `time_limits` - time limits for simulations depending on parameter for research. For linear plots, you use different time steps, but for statistical analysis data should have the same time period. Dictionary keys of the first level are simular with `mode`, the second level are simular with `dataset` from **/settings/mcluster.py** or **/settings/mlocal.py**;
    - `psets` - if your datasets or model simulations have *strange* time format you have to add correct time values in it. Otherwise you can ignore this step;
4. **/libraries/lib4colors.py** and add your new data to:
    - `xfire_colors` - colors and styles for linear plots;
5. **/libraries/lib4xarray.py** and add information about new dataset or model simulations to:
    - `get_data` - algorithm for data reading and initial convertation. Also you can add your personal algorithm for units convertation. In case of new model simulations, you can create an additional function for data reading similar with `read_ocn`, `read_jules` or `read_orchidee`.
    - `get_interpol` - algorithm for reinterplotation your data to OCN grid. (Important)

P.S.: The **/settings/mcluster.py**, **/settings/mlocal.py**, **/settings/path_settings.py** and **/libraries/lib4xarray.py** modules can be running independetly from other project scripts that gives you a change to control your user and path settings, and you can test data reading and reinterpolation algorithms before the main post-processing program. You can find more information about these modules in `readme.md` files from **/settings/** or **/libraries/** folders.








[1]: https://catalogue.ceda.ac.uk/uuid/3628cb2fdba443588155e15dee8e5352
[2]: https://climate.esa.int/en/projects/fire/news-and-events/news/global-detection-of-long-term-burned-area-with-avhrr-ltdr-data/
[2b]: https://www.sciencedirect.com/science/article/pii/S030324342100180X?via%3Dihub
[3]: https://daac.ornl.gov/VEGETATION/guides/fire_emissions_v4_R1.html
[4]: https://gmd.copernicus.org/articles/15/8411/2022/gmd-15-8411-2022-discussion.html
[5]: https://lpdaac.usgs.gov/products/mod17a2hgfv061/
[6]: https://lpdaac.usgs.gov/products/mod17a3hgfv061/
[9]: https://zenodo.org/record/4700264

[12a]: https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2009GB003521
[12b]: https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2009GB003522

[13a]: https://jules.jchmr.org/

[14a]: https://www.researchgate.net/publication/224943015_A_dynamic_global_vegetation_model_for_studies_of_the_coupled_atmosphere-biosphere_system
[14b]: https://www.pnas.org/doi/10.1073/pnas.0707213104
[14c]: https://orchidee.ipsl.fr/