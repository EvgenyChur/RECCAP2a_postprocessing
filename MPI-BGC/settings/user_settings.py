# -*- coding: utf-8 -*-
__all__ = [
    'logical_settings',
    'lcalc_settings',
    'get_settigs4_annual_plots',
    'get_settings4maps',
    'get_settings4diff_data',
    'get_settings4ds_time_limits',
    'get_settings4ocn_orc_ndep',
    'get_settings4domains',
    'get_settings4stations',
    'get_limits4annual_plots',
    'get_limits4station_plots',
    'get_settigs4maps',
    'get_settigs4maps_diff',
    'get_settigs4subplots',
    'get_settings4reccap2_domains',
    'get_settings4plots',
    'get_settings4plots_pft',
    'get_settings4plots_landcover',
    'get_ocn_pft',
    'get_modis_pft',
]
"""
The module has user settings for visualization:

The full list of OCN simulations:
    Fire simulations prepared by Ana Bastos: 
        OCN_S2.1, OCN_S2.2, OCN_S2.1.1, OCN_S3.1, OCN_S3.2
        
    None fire simulations prepared by Ana Bastos:
        'OCN_S2.1_nf', 'OCN_S3.1_nf'
    
    Fire simulations prepared by Evgenii Churiulin *(v202210) ERA5 (1950 - 2020)
        'OCN_S0'    , 'OCN_S2Prog'   , 'OCN_S2Diag'   ,
        
    Fire simulations prepared by Evgenii Churiulin *(v202302) ERA5 (1960 - 2022)
        'OCN_S0_v3' , 'OCN_S2Prog_v3', 'OCN_S2Diag_v3', 'OCN_Spost_v3'

    Fire simulations prepared by Evgenii Churiulin *(v202309) ERA5 (1960 - 2023)
        'OCN_S0_v4' , 'OCN_S2Prog_v4', 'OCN_S2Diag_v4', 'OCN_Spost_v4'

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
    1.5    2023-10-24 Evgenii Churiulin, MPI-BGC
           Added new OCN simulations
    1.6    2023-11-09 Evgenii Churiulin, MPI-BGC
           Added functions and new config class with user settings
"""
# =============================     Import modules     ==================
import config as cnf
from typing import Optional

# =============================   Personal functions   ==================

# ================   User settings (have to be adapted)  ================

# Section: Logical settings:
# ======================================================================
# -- Main logical settings for the project:
def logical_settings(**kwargs) -> dict:
    """User logical settings:
       Set logical parameters for computations. Most of the scripts from the project,
       use this logical settings. You can control the logical settings from your
       scripts using the next keys:

       lcluster = True / False
       lnc_info = True / False
       station_mode = True / False
       lvis_lines = True / False
       lBasemap_moment = True / False

       also, you can ignore all these keys. In that case, function will uses the
       default values equal to False

       In advance: You can add next command to your script
       print(settings.user_settings_doc.doc) and get more detailed information about
       input parameters. The most important parameter is **lcluster**
    """
    # -- Local variables:
    default = False

    def get_act_values(default_values:str, new_values:Optional[str] = None):
        """Set values for logical dictionary:"""
        return new_values if new_values != None else default_values

    # -- Logical settings:
    lsettings = {
        # Do you want to calculate on cluster?
        'lcluster'       : get_act_values(default, kwargs.get('lcluster')),
        # Do you want to get more information about NetCDF data?
        'lnc_info'       : get_act_values(default, kwargs.get('lnc_info')),
        # Do you want to get values for stations?
        'station_mode'   : get_act_values(default, kwargs.get('station_mode')),
        # Do you want to visualize data (line plots)?
        'lvis_lines'     : get_act_values(default, kwargs.get('lvis_lines')),
        # Do you want to visualize data on grid for one moment?
        'lBasemap_moment': get_act_values(default, kwargs.get('lBasemap_moment')),
    }
    return lsettings


# -- Additional logical parameters for the 2D maps (important for fire_xarray.py)
def lcalc_settings(**kwargs) -> dict:
    """Calculation settings:
       Set logical parameters for computations and visualization. These parameters
       are important for fire_xarray.py script or when lBasemap_moment is True.
       You can control the logical settings  from your scripts using the next keys:

        lmean_calc
        lstd_calc
        ltrend_calc
        ldiff_calc
        lmean_plot
        lstd_plot
        ltrend_plot
        lcollage
        ldiff_plot

        also, you can ignore all these keys. In that case, function will uses the
        default values equal to False

        In advance: You can add next command to your script
        print(settings.user_settings_doc.doc) and get more detailed information about
        input parameters.
    """
    # -- Local variables:
    default = False
    def get_act_values(default_values:str, new_values:Optional[str] = None):
        """Set values for logical dictionary:"""
        return new_values if new_values != None else default_values

    # -- Calculation settings:
    calc_settings = {
        # Activate algorithm for mean, std, time trend calculations?
        'lstat'  : get_act_values(default, kwargs.get('lstat')),
        # Activate algorithm for mean visualization (one figure)?
        'lmean_plot'  : get_act_values(default, kwargs.get('lmean_plot')),
        # Activate algorithm for std visualization (one figure)?
        'lstd_plot'   : get_act_values(default, kwargs.get('lstd_plot')),
        # Activate algorithm for trends visualization (one figure)?
        'ltrend_plot' : get_act_values(default, kwargs.get('ltrend_plot')),
        # Activate algorithm for collage plots: mean, std, trend
        'lcollage'    : get_act_values(default, kwargs.get('lcollage')),
        # Activate algorithm for difference calculations?
        'ldiff_calc'  : get_act_values(default, kwargs.get('ldiff_calc')),
    }
    return calc_settings


# Section 0: Main user settings for work:
# ======================================================================
# -- 0.1: Select datasets which you want to figure out on your linear plots
def get_settigs4_annual_plots(
        lline_plot:bool, lmap_plot:bool, **kwargs) -> tuple[dict, dict]:
    # -- Local variables:
    refer_tstart = 1980
    refer_tstop = 2024
    # -- Create time period for datasets:
    t1 = kwargs.get('tstart') if 'tstart' in kwargs else refer_tstart
    t2 = kwargs.get('tstop')  if 'tstop'  in kwargs else refer_tstop

    if lline_plot and lmap_plot is False:
        # -- OCN simulations:
        ocn_sim = ['OCN_S2Prog_v4', 'OCN_S2Diag_v4']
        # -- JULES simulations:
        jul_sim = ['JUL_S2Prog', 'JUL_S2Diag']
        # -- ORCHIDEE simulations:
        orc_sim = ['ORC_S2Prog', 'ORC_S2Diag']
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
        return av_datasets
    else:
        if ((lline_plot and lmap_plot) or
            (lline_plot is False and lmap_plot is False)):
            raise ValueError('lline_plot and lmap_plot cannot be activated or deactivated together')


# -- 0.2: Select datasets which you want to figure out on your 2D maps
def get_settings4maps(
    lline_plot:bool, lmap_plot:bool, **kwargs) -> tuple[dict, dict]:
    # -- Local variables:
    refer_tstart = 2003
    refer_tstop = 2020
    # -- Create time period for datasets:
    t1 = kwargs.get('tstart') if 'tstart' in kwargs else refer_tstart
    t2 = kwargs.get('tstop')  if 'tstop'  in kwargs else refer_tstop
    # -- Define datasets:
    if lline_plot is False and lmap_plot:
        # -- OCN simulations:
        ocn_sim = ['OCN_S2Prog_v4', 'OCN_S2Diag_v4']
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
        return av_datasets
    else:
        if ((lline_plot and lmap_plot) or
            (lline_plot is False and lmap_plot is False)):
            raise ValueError('lline_plot and lmap_plot cannot be activated or deactivated together')


# -- 0.3 Select reference and comparison datasets for DIFFERENCE 2Dmaps:
def get_settings4diff_data(
        basic_ds4refer: Optional[str] = 'OCN_S2Prog_v4', # Standard dataset for reference
        basic_ds4comp: Optional[str] = 'OCN_S2Diag_v4',  # Standard dataset for comparison
        **kwargs,
    ) -> dict:
    """Settings for difference metrics (diff = refer - comp_ds):

        If you want to add new reference or comparison dataset you have to use:
           ba_, ffire_, lai_, cveg_, npp_, gpp_, nbp_, nee_ keywords with
           postfix **refer** or **comp** (without **)"""
    # -- Uniq reference dataset:
    def get_ds4refer(standard_refer:str, refer: Optional[str] = None):
        return refer if refer != None else standard_refer

    # -- Uniq dataset for comparison:
    def get_ds4comp(standard_ds4comp:str, ds4comp: Optional[str] = None, ):
        return ds4comp if ds4comp != None else standard_ds4comp

    # -- Select reference and comparison datsets:
    diff_options = {
        'burned_area' : [
            get_ds4refer(basic_ds4refer, kwargs.get('ba_refer')),
            get_ds4comp(basic_ds4comp  , kwargs.get('ba_comp'))],
        'fFire' : [
            get_ds4refer(basic_ds4refer, kwargs.get('ffire_refer')),
            get_ds4comp(basic_ds4comp  , kwargs.get('ffire_comp'))],
        'lai' : [
            get_ds4refer(basic_ds4refer, kwargs.get('lai_refer')),
            get_ds4comp(basic_ds4comp  , kwargs.get('lai_comp'))],
        'cVeg' : [
            get_ds4refer(basic_ds4refer, kwargs.get('cveg_refer')),
            get_ds4comp(basic_ds4comp  , kwargs.get('cveg_comp'))],
        'npp' : [
            get_ds4refer(basic_ds4refer, kwargs.get('npp_refer')),
            get_ds4comp(basic_ds4comp  , kwargs.get('npp_comp'))],
        'gpp' : [
            get_ds4refer(basic_ds4refer, kwargs.get('gpp_refer')),
            get_ds4comp(basic_ds4comp  , kwargs.get('gpp_comp'))],
        'nee' : [
            get_ds4refer(basic_ds4refer, kwargs.get('nee_refer')),
            get_ds4comp(basic_ds4comp, kwargs.get('nee_comp'))],
        'nbp' : [
            get_ds4refer(basic_ds4refer, kwargs.get('nbp_refer')),
            get_ds4comp(basic_ds4comp, kwargs.get('npb_comp'))],
    }
    return diff_options


# Section 1: Settings for datasets:
# ======================================================================
# 1.1: Get time limits for datasets. These settings allow to control the time
#      slice for research dataset (Important for statistical parameters):
def get_settings4ds_time_limits(uconfig:cnf) -> dict:
    """User settings for time slice of datasets. Important for statistical computations:"""
    return uconfig.get('time_limits')


# 1.2: Get time axis settings for OCN, ORCHIDEE and NDEP simulations and datasets
def get_settings4ocn_orc_ndep(uconfig:cnf) -> dict:
    """User time settings for OCN, ORCHIDEE and NDEP input data"""
    return uconfig.get('time_axis_settings')


# Section 2: Settings for DOMAINS (lat1, lat2, lon1, lon2):
# ======================================================================
def get_settings4domains(uconfig:cnf) -> dict:
    """ User settings for research domains:"""
    return uconfig.get('domain_lim')


# Section 3: Settings for STATIONS (lat,lon, st_name, OCN_PFT):
# ======================================================================
def get_settings4stations(uconfig:cnf) -> dict:
    """User settings for stations"""
    return uconfig.get('stations')


# Section 4: Settings for annual linear plots:
# ======================================================================
# -- 4.1: Linear plots for domains:
def get_limits4annual_plots(start_year:int, uconfig:cnf) -> dict:
    """Get user settings for Y axis depending on first year"""
    # -- Local variables:
    t1, t2, t3 = 1960, 1980, 2003
    # -- Set limits for linear plots depending on current period:
    if (start_year >= t1) and (start_year < t2):
        ann_plot_limits = uconfig.get('annual_plots_since_1960')
    elif (start_year >= t2) and (start_year < t3):
        ann_plot_limits = uconfig.get('annual_plots_since_1980')
    elif (start_year >= t3):
        ann_plot_limits = uconfig.get('annual_plots_since_2003')
    else: # Wildcard:
        raise TimeoutError('Incorrect time format')
    return ann_plot_limits


# -- 4.2: Linear plots for stations:
def get_limits4station_plots(start_year:int, uconfig:cnf) -> dict:
    """Get user settings for Y axis depending on first year"""
    # -- Local variables:
    t1, t2, t3 = 1960, 1980, 2003
    # -- Set limits for linear plots depending on current period:
    if (start_year >= t1) and (start_year < t2):
        ann_stat_limits = uconfig.get('annual_plots4stations_since_1960')
    elif (start_year >= t2) and (start_year < t3):
        ann_stat_limits = uconfig.get('annual_plots4stations_since_1980')
    elif (start_year >= t3):
        ann_stat_limits = uconfig.get('annual_plots4stations_since_2003')
    else: # Wildcard:
        raise TimeoutError('Incorrect time format')
    return ann_stat_limits

# Section 5: Settings for 2D maps (mean, std, trend plots):
# =====================================================================
def get_settigs4maps(uconfig:cnf) -> dict:
    """Get domains properties from config file for 2D Maps (mean, std, trend)"""
    return {
        'Global' : uconfig.get('clb_limits_GTO'),
        'Europe' : uconfig.get('clb_limits_EN'),
        'Tropics': uconfig.get('clb_limits_GTO'),
        'NH'     : uconfig.get('clb_limits_EN'),  # not optimized
        'Other'  : uconfig.get('clb_limits_GTO'), # not optimized
    }


# Section 6: Settings for 2D maps (DIFF plots):
# =====================================================================
def get_settigs4maps_diff(uconfig:cnf) -> dict:
    """Get domains properties from config file for 2D DIFF MAPS (mean, std, trend)"""
    return {
        'Global' : uconfig.get('clb_diff_limits_GTO'),
        'Europe' : uconfig.get('clb_diff_limits_EN'),
        'Tropics': uconfig.get('clb_diff_limits_GTO'),
        'NH'     : uconfig.get('clb_diff_limits_EN'),  # not optimized
        'Other'  : uconfig.get('clb_diff_limits_GTO'), # not optimized
    }


# Section 7: Settings for subplots
# ======================================================================
def get_settigs4subplots(uconfig:cnf) -> dict:
    """Get user settings for subplots"""
    return {
        'Global' : uconfig.get('layout_settings_moll'),
        'Europe' : uconfig.get('layout_settings_merc'),
        'Tropics': uconfig.get('layout_settings_cyl'),
        'NH'     : uconfig.get('layout_settings_cyl'), # not optimized
        'Other'  : uconfig.get('layout_settings_merc'), # not optimized
    }


# Section 8: Settings for RECCAP2 domain (linear plots limits)
# ======================================================================
def get_settings4reccap2_domains(uconfig:cnf) -> dict:
    """Get user settings for RECCAP2 domains"""
    return uconfig.get('limits4reccap2_domains')


# Section 9: User settings for linear plots (color, style, hatches)
# ======================================================================
# -- 9.1: Colors for research simulations and datasets:
def get_settings4plots(uconfig:cnf) -> dict:
    """Get user settings for plots (line color, style and hatches):"""
    return uconfig.get('xfire_colors')


# -- 9.2: Linear plots for check_ocn_pft script:
def get_settings4plots_pft(uconfig:cnf) -> dict:
    """User settings for PFT plots:"""
    return uconfig.get('check_colors')


# -- 9.3: Linear plots for landcover script:
def get_settings4plots_landcover(uconfig:cnf) -> dict:
    """User settings for landcover plots:"""
    return uconfig.get('ln_colors')

# Section 10: User settings for PFT:
# ======================================================================
# 10.1 Load OCN-PFT:
def get_ocn_pft(uconfig:cnf) -> list[dict]:
    """User settings for OCN PFT:"""
    return uconfig.get('ocn_pft')

# 10.2 Load MODIS-PFT:
def get_modis_pft(uconfig:cnf) -> list[dict]:
    """User settings for MODIS PFT:"""
    return uconfig.get('modis_pft')


# -- Simple tests:
if __name__ == '__main__':
    bcc = cnf.Bulder_config_class()
    tlm = bcc.user_settings()
    # Check dataset limits:
    test1_1 = get_settings4ds_time_limits(tlm)

    # Check values from section 9:
    test9_1 = get_settings4plots(tlm)
    test9_2 = get_settings4plots_pft(tlm)
    test9_3 = get_settings4plots_landcover(tlm)

    # -- Print values:
    print('get_settings4ds_time_limits \n', test1_1, '\n')
    print('get_settings4plots \n', test9_1, '\n')
    print('get_settings4plots_pft \n', test9_2, '\n')
    print('get_settings4plots_landcover \n', test9_3, '\n')
