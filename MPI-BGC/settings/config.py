# -*- coding: utf-8 -*-
"""
Description: The configuration file with user settings

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    09.11.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""
from creator_dict4maps import Map_settings
from typing import Optional


class config_class:
    def __init__(self):
        """
        """
        self.values = {}

    def add(self, key, values):
        """
        """
        self.values[key] = values

    def get(self, key):
        """
        """
        return self.values[key]


class Bulder_config_class:
    """Configurator of user settings:"""
    def __init__(self, **kwargs):
        # -- Time limits for datasets:
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
        self.tstart = 0
        self.tstop  = 1
        self.tp_ocn = self.__ocn_refer(kwargs.get('ocn'))
        self.tp_jul = self.__jul_refer(kwargs.get('jul'))
        self.tp_orc = self.__orc_refer(kwargs.get('jul'))
        self.tp_gfed41s = self.__gfed41s_refer(kwargs.get('gfed41s'))
        self.tp_modis = self.__modis_refer(kwargs.get('modis'))
        self.tp_gfed_tot = self.__gfed_tot_refer(kwargs.get('gfed_tot'))
        self.tp_gfed_fl = self.__gfed_fl_refer(kwargs.get('gfed_fl'))
        self.tp_avhrr = self.__avhrr_refer(kwargs.get('avhrr'))
        self.tp_mod17a2 = self.__mod17a2_refer(kwargs.get('mod17a2'))
        self.tp_mod17a3 = self.__mod17a3_refer(kwargs.get('mod17a3'))
        self.tp_globmap = self.__globmap_refer(kwargs.get('globmap'))
        self.tp_ltdr = self.__ltdr_refer(kwargs.get('ltdr'))

        # -- Time settings for OCN datasets (have incorrect time axis):
        self.ocn_init_1850 = '1850-01-01'
        self.ocn_init_1950 = '1950-01-01'
        self.ocn_init_1960 = '1960-01-01'
        self.ocn_init_2000 = '2000-01-01'
        self.ocn_init_2003 = '2003-01-01'
        self.ocn_end_2021 = '2021-01-01'
        self.ocn_end_2022 = '2022-01-01'
        self.ocn_end_2023 = '2023-01-01'
        self.ocn_end_2024 = '2024-01-01'
        self.ocn_freq = '1M' 
        # -- Time settings for ORCHIDEE datasets (have incorrect time axis):
        self.orc_init_1960 = '1960-01-01'
        self.orc_init_2003 = '2003-01-01'
        self.orc_end_2021  = '2021-01-01'
        self.orc_freq = '1M'
        # -- Time settings for NDEP simulation:
        self.ndep_init = '2018-01-01'
        self.ndep_end  = '2018-12-01'
        self.ndep_freq = '1MS'
        # -- Zero values
        self.zero = 0.0

    # -- Quality control of input data
    def __verify_input_period(func):
        def verification(self, *args, **kwargs):
            lst_period = func(self, *args, **kwargs)
            if type(lst_period) != list:
                raise TypeError('Dataset period has to be a list')
            if len(lst_period) != 2:
                raise TypeError('Dataset period has to be presented as a list with 2 elements')
            if type(lst_period[0]) != int:
                raise TypeError('Start year should be a int')
            if type(lst_period[1]) != int:
                raise TypeError('End year should be a int')
            return lst_period
        return verification

    @__verify_input_period
    def __ocn_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for OCN data or use default values"""
        default_limits = [1980, 2024]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __jul_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for JULES data or use default values"""
        default_limits = [1980, 2024]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __orc_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for ORCHIDEE data or use default values"""
        default_limits = [1980, 2024]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __modis_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for MODIS data or use default values"""
        default_limits = [2003, 2020]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __gfed41s_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for GFED4.1s data or use default values"""
        default_limits = [2003, 2016] # 2020 for fFire
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __gfed_tot_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for GFED_TOT data or use default values"""
        default_limits = [2003, 2020]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __gfed_fl_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for GFED_FL data or use default values"""
        default_limits = [2003, 2020]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __avhrr_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for AVHRR data or use default values"""
        default_limits = [2003, 2016] # 2020
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __mod17a2_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for MOD17A2 data or use default values"""
        default_limits = [2003, 2020]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __mod17a3_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for MOD17A3 data or use default values"""
        default_limits = [2003, 2020]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __globmap_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for GLOBMAP data or use default values"""
        default_limits = [2003, 2020]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits

    @__verify_input_period
    def __ltdr_refer(self, ulimits: Optional[list[int,int]] = None):
        """User can select uniq time period for LTDR data or use default values"""
        default_limits = [2003, 2020]
        ds_tlimits = ulimits if ulimits != None else default_limits
        return ds_tlimits


    def user_settings(self) -> dict:
        """User settings for RECCAP2 project:"""
        cfg = config_class()
        
        # Section 1: Datasets time settings:
        # =====================================================================
        # -- 1.1: Time limits for simulations depending on parameter for research:
        #         Datasets have different time perios. You have to choose your time
        #         periods for datasets. Also, the x-axis limits for linear plots depending
        #         on OCN values.
        cfg.add(
            'time_limits',{
                'burned_area' : {
                    'GFED4.1s' : [
                        self.tp_gfed41s[self.tstart], self.tp_gfed41s[self.tstop]],
                    'GFED_TOT' : [
                        self.tp_gfed_tot[self.tstart], self.tp_gfed_tot[self.tstop]],
                    'GFED_FL' : [
                        self.tp_gfed_fl[self.tstart], self.tp_gfed_fl[self.tstop]],
                    'BA_MODIS' : [
                        self.tp_modis[self.tstart], self.tp_modis[self.tstop]],
                    'BA_AVHRR' : [
                        self.tp_avhrr[self.tstart], self.tp_avhrr[self.tstop]],
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    'JUL' : [self.tp_jul[self.tstart], self.tp_jul[self.tstop]],
                    'ORC' : [self.tp_orc[self.tstart], self.tp_orc[self.tstop]],
                    },
                'fFire' : {
                    'GFED4.1s' : [
                        self.tp_gfed41s[self.tstart] , self.tp_gfed41s[self.tstop]],
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    'JUL' : [self.tp_jul[self.tstart], self.tp_jul[self.tstop]],
                    'ORC' : [self.tp_orc[self.tstart], self.tp_orc[self.tstop]],
                    },
                'lai' : {
                    'LAI_LTDR' : [
                        self.tp_ltdr[self.tstart], self.tp_ltdr[self.tstart]],
                    'LAI_MODIS': [
                        self.tp_modis[self.tstart], self.tp_modis[self.tstop]],
                    'GLOBMAP'  : [
                        self.tp_globmap[self.tstart] , self.tp_globmap[self.tstart]],
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    'JUL' : [self.tp_jul[self.tstart], self.tp_jul[self.tstop]],
                    'ORC' : [self.tp_orc[self.tstart], self.tp_orc[self.tstop]],
                    },
                'cVeg' : {
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    'JUL' : [self.tp_jul[self.tstart], self.tp_jul[self.tstop]],
                    'ORC' : [self.tp_orc[self.tstart], self.tp_orc[self.tstop]],
                    },
                'npp' : {
                    'MOD17A3' : [
                        self.tp_mod17a3[self.tstart] , self.tp_mod17a3[self.tstop]],
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    'JUL' : [self.tp_jul[self.tstart], self.tp_jul[self.tstop]],
                    },
                'gpp' : {
                    'MOD17A2' : [
                        self.tp_mod17a2[self.tstart] , self.tp_mod17a2[self.tstop]],
                    'MOD17A3' : [
                        self.tp_mod17a3[self.tstart] , self.tp_mod17a3[self.tstop]],
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    'JUL' : [self.tp_jul[self.tstart], self.tp_jul[self.tstop]],
                    'ORC' : [self.tp_orc[self.tstart], self.tp_orc[self.tstop]],
                    },
                'nee' : {
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    },
                'nbp' : {
                    'OCN' : [self.tp_ocn[self.tstart], self.tp_ocn[self.tstop]],
                    'JUL' : [self.tp_jul[self.tstart], self.tp_jul[self.tstop]],
                    'ORC' : [self.tp_orc[self.tstart], self.tp_orc[self.tstop]],
                    },
            }
        )

        # -- 1.2: Time ranges for OCN simulations (OCN datasets have incorrect time axis):
        cfg.add(
            "time_axis_settings", {
                # -- OCN simulations based on Ana's Bastos experiment:
                'OCN_S2.1' : [
                    self.ocn_init_1950, self.ocn_end_2022, self.ocn_freq],
                'OCN_S2.2' : [
                    self.ocn_init_1950, self.ocn_end_2022, self.ocn_freq],
                'OCN_S3.1' : [
                    self.ocn_init_1950, self.ocn_end_2022, self.ocn_freq],
                'OCN_S3.2' : [
                    self.ocn_init_1950, self.ocn_end_2022, self.ocn_freq],
                'OCN_S2.1_nf' : [
                    self.ocn_init_1950, self.ocn_end_2022, self.ocn_freq],
                'OCN_S3.1_nf' : [
                    self.ocn_init_1950, self.ocn_end_2022, self.ocn_freq],
                'OCN_S2.1.1' : [
                    self.ocn_init_1950, self.ocn_end_2023, self.ocn_freq],
                # -- OCN simulations based on v202209 model run:
                'OCN_S0' : [
                    self.ocn_init_1950, self.ocn_end_2021, self.ocn_freq],
                'OCN_S2Prog' : [
                    self.ocn_init_1950, self.ocn_end_2021, self.ocn_freq],
                'OCN_S2Diag' : [
                    self.ocn_init_2000, self.ocn_end_2021, self.ocn_freq],
                # -- OCN simulations based on v202302 model run:
                'OCN_Spost_v3' : [
                    self.ocn_init_1850, self.ocn_end_2021, self.ocn_freq],
                'OCN_S0_v3' : [
                    self.ocn_init_1960, self.ocn_end_2021, self.ocn_freq],
                'OCN_S2Prog_v3' : [
                    self.ocn_init_1960, self.ocn_end_2023, self.ocn_freq],
                'OCN_S2Diag_v3' : [
                    self.ocn_init_2003, self.ocn_end_2021, self.ocn_freq],
                # -- OCN simulations based on v202309 model run:
                'OCN_Spost_v4' : [
                    self.ocn_init_1850, self.ocn_end_2021, self.ocn_freq],
                'OCN_S0_v4' : [
                    self.ocn_init_1960, self.ocn_end_2021, self.ocn_freq],
                'OCN_S2Prog_v4' : [
                    self.ocn_init_1960, self.ocn_end_2024, self.ocn_freq],
                'OCN_S2Diag_v4' : [
                    self.ocn_init_2003, self.ocn_end_2021, self.ocn_freq],
                # -- ORCHIDEE simulations:
                'ORC_S0' : [
                    self.orc_init_1960, self.orc_end_2021, self.ocn_freq],
                'ORC_S2Prog' : [
                    self.orc_init_1960, self.orc_end_2021, self.ocn_freq],
                'ORC_S2Diag' : [
                    self.orc_init_2003, self.orc_end_2021, self.ocn_freq],
                # -- Other datasets:
                'NDEP' : [
                    '2018-01-01', '2018-12-01', '1MS'],
            }
        )

        # Section 2: Domain settings:
        # =====================================================================
        # -- 2.1: Datasets have different spatial resolution. For example: the datasets
        #         MODIS, AVHRR and GFED have grids: lat (-90 : 90) and lon (-180 : 180),
        #         however the OCN grids are: (-60 : 90) and (-180 : 180). Because of that
        #         it is really important to get the simular coordinates
        #         before - interpolation. Otherwise, the model grid will be irregular.
        cfg.add(
            'domain_lim', {
                # Domain    lat start  lat stop  lon start   lon stop
                'Global' : [   90.0  ,   -60.0 ,   -180.0 ,   180.0  ],
                'Europe' : [   72.0  ,    34.0 ,    -10.0 ,    45.0  ],
                'Tropics': [   23.0  ,   -23.0 ,   -180.0 ,   180.0  ],
                'NH'     : [   80.0  ,    30.0 ,   -180.0 ,   180.0  ],
                'Other'  : [   90.0  ,   -90.0 ,   -180.0 ,   180.0  ],
            }
        )

        # Section 3: Station settings:
        # =====================================================================
        # -- 3.1: There is option for analysis of data in a special point.
        #         You can add your point in this section.
        cfg.add(
            'stations', {
            # Point     lat    lon   Place                        OCN PFT
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
        )

        # Section 4: Annual plots settings (limits for axis):
        # =====================================================================
        # -- 4.1: User limits for annual plots from 1960 to current time:
        cfg.add(
            'annual_plots_since_1960', {
                # Region
                'Global' : {
                    #  VAR              ymin    ymax     ystep
                    'burned_area' : [  2000.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   400.0,   650.1,   25.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   110.0,   200.1,   10.0 ],
                    'npp'         : [    60.0,   100.1,    5.0 ],
                    'nee'         : [    -7.0,     0.1,    1.0 ],
                    'nbp'         : [    -2.0,     6.1,    1.0 ],
                    'fFire'       : [     0.0,     7.1,    1.0 ],
                },
                'Europe' : {
                    'burned_area' : [     0.0,   140.1,   10.0 ],
                    'cVeg'        : [    20.0,    60.1,    5.0 ],
                    'lai'         : [     0.0,     3.6,    0.5 ],
                    'gpp'         : [     5.0,    14.51,   0.5 ],
                    'npp'         : [     5.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.01,   0.2 ],
                    'nbp'         : [    -1.0,     0.81,   0.2 ],
                    'fFire'       : [     0.0,     0.17,   0.02],
                },  
                'Tropics': {
                    'burned_area' : [  2500.0,  9500.1, 1000.0 ],
                    'cVeg'        : [   200.0,   400.1,   25.0 ],
                    'lai'         : [     0.0,     1.21,   0.1 ],
                    'gpp'         : [    60.0,   130.1,   10.0 ],
                    'npp'         : [    30.0,    70.1,    5.0 ],
                    'nee'         : [    -4.0,     2.1,    1.0 ],
                    'nbp'         : [    -5.0,     4.1,    1.0 ],
                    'fFire'       : [     0.0,     6.1,    1.0 ],
                },
                # (not optimized)
                'NH'     : {
                    'burned_area' : [   200.0,  1200.1,  200.0 ],
                    'cVeg'        : [    20.0,    40.1,    5.0 ],
                    'lai'         : [     0.0,     3.1,    0.2 ],
                    'gpp'         : [    10.0,    15.1,    1.0 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.5,    0.2 ],
                    'nbp'         : [    -0.2,     1.5,    0.2 ],
                    'fFire'       : [     0.0,     0.2,    0.02],
                },
                # (not optimized)
                'Other'  : {
                    'burned_area' : [  3500.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   450.0,   750.1,   50.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   180.1,   10.0 ],
                    'npp'         : [    65.0,    95.1,    5.0 ],
                    'nee'         : [    -7.0,     3.1,    1.0 ],
                    'nbp'         : [    -4.0,     8.1,    2.0 ],
                    'fFire'       : [     0.0,     8.1,    2.0 ],
                },
            }
        )
        # -- 4.2: User limits for annual plots from 1980 to current time:
        cfg.add(
            'annual_plots_since_1980', {
                # Region
                'Global' : {
                    #  VAR              ymin    ymax     ystep
                    'burned_area' : [  2000.0, 11000.1, 1000.0 ],
                    'cVeg'        : [   400.0,   675.1,   25.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   200.1,   10.0 ],
                    'npp'         : [    70.0,   105.1,    5.0 ],
                    'nee'         : [    -7.0,    -2.1,    0.5 ],
                    'nbp'         : [    -4.0,     6.1,    2.0 ],
                    'fFire'       : [     0.0,     5.1,    1.0 ],
                },
                'Europe' : {
                    'burned_area' : [     0.0,   200.1,   20.0 ],
                    'cVeg'        : [    20.0,    65.1,    5.0 ],
                    'lai'         : [     0.0,     3.6,    0.5 ],
                    'gpp'         : [     5.0,    15.1,    2.5 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,    -0.21,   0.2 ],
                    'nbp'         : [    -0.6,     0.81,   0.2 ],
                    'fFire'       : [     0.0,     0.17,   0.02],
                },
                'Tropics': {
                    'burned_area' : [  2500.0,  9500.1, 1000.0 ],
                    'cVeg'        : [   200.0,   400.1,   25.0 ],
                    'lai'         : [     0.0,     1.21,   0.1 ],
                    'gpp'         : [    70.0,   130.1,   10.0 ],
                    'npp'         : [    34.0,    60.1,    5.0 ],
                    'nee'         : [    -4.0,     0.1,    1.0 ],
                    'nbp'         : [    -6.0,     4.1,    1.0 ],
                    'fFire'       : [     0.0,     5.1,    1.0 ]
                }, 
                # (not optimized)
                'NH'     : {
                    'burned_area' : [   200.0,  1200.1,  200.0 ],
                    'cVeg'        : [    20.0,    40.1,    5.0 ],
                    'lai'         : [     0.0,     3.1,    0.2 ],
                    'gpp'         : [    10.0,    15.1,    1.0 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.5,    0.2 ],
                    'nbp'         : [    -0.2,     1.5,    0.2 ],
                    'fFire'       : [     0.0,     0.2,    0.02],
                }, 
                # (not optimized)
                'Other'  : {
                    'burned_area' : [  3500.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   450.0,   750.1,   50.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   180.1,   10.0 ],
                    'npp'         : [    65.0,    95.1,    5.0 ],
                    'nee'         : [    -7.0,     3.1,    1.0 ],
                    'nbp'         : [    -4.0,     8.1,    2.0 ],
                    'fFire'       : [     0.0,     8.1,    2.0 ],
                },
            }
        )
        # -- 4.3: User limits for annual plots from 2003 to current time:
        cfg.add(
            'annual_plots_since_2003', {
                # Region
                'Global' : {
                    # Mode             ymin      ymax     ystep
                    'burned_area' : [  2000.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   400.0,   650.1,   25.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   130.0,   250.1,   10.0 ],
                    'npp'         : [    70.0,   100.1,    5.0 ],
                    'nee'         : [    -7.0,    -2.1,    1.0 ],
                    'nbp'         : [    -2.0,     5.1,    1.0 ],
                    'fFire'       : [     0.0,     5.1,    1.0 ],
                },
                'Europe' : {
                    'burned_area' : [     0.0,   180.1,   20.0 ],
                    'cVeg'        : [    30.0,    70.1,   10.0 ],
                    'lai'         : [     0.0,     3.6,    0.5 ],
                    'gpp'         : [     6.0,    14.51,   0.5 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.01,   0.2 ],
                    'nbp'         : [    -1.0,     0.81,   0.2 ],
                    'fFire'       : [    -0.05,    0.21,   0.05],
                },   
                'Tropics': {
                    'burned_area' : [  2500.0,  9500.1, 1000.0 ],
                    'cVeg'        : [   200.0,   400.1,   25.0 ],
                    'lai'         : [     0.0,     1.21,   0.1 ],
                    'gpp'         : [    70.0,   150.1,   10.0 ],
                    'npp'         : [    35.0,    70.1,    5.0 ],
                    'nee'         : [    -4.0,     0.1,    1.0 ],
                    'nbp'         : [    -5.0,     3.1,    1.0 ],
                    'fFire'       : [     0.0,     4.1,    1.0 ],
                },
                # (not optimized)
                'NH' : {
                    'burned_area' : [   200.0,  1200.1,  200.0 ],
                    'cVeg'        : [    20.0,    40.1,    5.0 ],
                    'lai'         : [     0.0,     3.1,    0.2 ],
                    'gpp'         : [    10.0,    15.1,    1.0 ],
                    'npp'         : [     6.0,     8.1,    0.5 ],
                    'nee'         : [    -1.0,     0.5,    0.2 ],
                    'nbp'         : [    -0.2,     1.5,    0.2 ],
                    'fFire'       : [     0.0,     0.2,    0.02],
                },
                # (not optimized)
                'Other'  : {
                    'burned_area' : [  3500.0, 11500.1, 1000.0 ],
                    'cVeg'        : [   450.0,   750.1,   50.0 ],
                    'lai'         : [     0.0,     1.1,    0.1 ],
                    'gpp'         : [   120.0,   180.1,   10.0 ],
                    'npp'         : [    65.0,    95.1,    5.0 ],
                    'nee'         : [    -7.0,     3.1,    1.0 ],
                    'nbp'         : [    -4.0,     8.1,    2.0 ],
                    'fFire'       : [     0.0,     8.1,    2.0 ],
                },
            }
        )
        # -- 4.4: User limits for annual plots for stations from 1960 to current time:
        cfg.add(
            'annual_plots4stations_since_1960', {
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
        )
        # -- 4.5: User limits for annual plots for stations from 1960 to current time:
        cfg.add(
            'annual_plots4stations_since_1980', {
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
        )
        # -- 4.6: User limits for annual plots for stations from 1960 to current time:
        cfg.add(
            'annual_plots4stations_since_2003', {
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
        )

        # Section 5: 2D plots settings (limits for axis):
        # =====================================================================
        #  Settings for 2D plots (normal mode):
        # Actual matplotlib colormap are here:
        #    https://matplotlib.org/stable/tutorials/colors/colormaps.html

        # -- 5.1:Colorbar settings for data over 'Global', 'Tropics', 'Other' regions:
        # -- Burned area properties:
        ba_mean_creator = Map_settings( 'burned_area', 'mean' ,  0.0 , 0.30, 'hot_r' )
        ba_std_creator = Map_settings(  'burned_area', 'std'  ,  0.0 , 0.10, 'hot_r' )
        ba_trend_creator = Map_settings('burned_area', 'trend', -1e-3, 1e-3, 'RdBu_r')
        # -- cVeg properties:
        cveg_mean_creator = Map_settings( 'cVeg', 'mean' ,   0.0, 20.0 , 'gist_earth_r')
        cveg_std_creator = Map_settings(  'cVeg', 'std'  ,   0.0,  2.0 , 'gist_earth_r')
        cveg_trend_creator = Map_settings('cVeg', 'trend', -0.04,  0.04, 'RdBu_r')
        # -- GPP properties (Gross Primary Production):
        gpp_mean_creator = Map_settings( 'gpp', 'mean' ,   0.0, 4000.0, 'gist_earth_r')
        gpp_std_creator = Map_settings(  'gpp', 'std'  ,   0.0,  400.0, 'gist_earth_r')
        gpp_trend_creator = Map_settings('gpp', 'trend', -10.0,   10.0, 'RdBu_r')
        # -- NPP properties (Net primary production):
        npp_mean_creator = Map_settings( 'npp', 'mean' ,   0.0, 1500.0, 'gist_earth_r')
        npp_std_creator = Map_settings(  'npp', 'std'  ,   0.0,  200.0, 'gist_earth_r')
        npp_trend_creator = Map_settings('npp', 'trend', -10.0,   10.0, 'RdBu_r')
        # -- LAI properties (Leaf Area Index):
        lai_mean_creator = Map_settings( 'lai', 'mean' ,   0.0 , 6.0  , 'Greens')
        lai_std_creator = Map_settings(  'lai', 'std'  ,   0.0 , 3.0  , 'Greens')
        lai_trend_creator = Map_settings('lai', 'trend',  -0.04, 0.04 , 'PRGn')
        # -- NEE properties (Net Ecosystem Exchange):
        nee_mean_creator = Map_settings( 'nee', 'mean' , -150.0,  50.0, 'PRGn')
        nee_std_creator = Map_settings(  'nee', 'std'  ,    0.0, 200.0, 'Greens')
        nee_trend_creator = Map_settings('nee', 'trend',   -2.0,   2.0, 'RdBu_r')
        # -- NPB properties (Net Biome Production):
        nbp_mean_creator = Map_settings( 'nbp', 'mean' ,  -60.0,  60.0, 'PRGn')
        nbp_std_creator = Map_settings(  'nbp', 'std'  ,    0.0, 150.0, 'Greens')
        nbp_trend_creator = Map_settings('nbp', 'trend',   -2.0,   2.0, 'RdBu_r')
        # -- fFire properties (CO2 Flux to Atmosphere from Fire):
        ffire_mean_creator = Map_settings( 'fFire', 'mean' ,  0.0, 80.0, 'hot_r')
        ffire_std_creator = Map_settings(  'fFire', 'std'  ,  0.0, 60.0, 'hot_r')
        ffire_trend_creator = Map_settings('fFire', 'trend', -0.4,  0.4, 'RdBu_r')
        # -- Create list of settings:
        cfg.add(
            'clb_limits_GTO', [
                ba_mean_creator.make_dict(),
                ba_std_creator.make_dict(),
                ba_trend_creator.make_dict(),
                cveg_mean_creator.make_dict(),
                cveg_std_creator.make_dict(),
                cveg_trend_creator.make_dict(),
                gpp_mean_creator.make_dict(),
                gpp_std_creator.make_dict(),
                gpp_trend_creator.make_dict(),
                npp_mean_creator.make_dict(),
                npp_std_creator.make_dict(),
                npp_trend_creator.make_dict(),
                lai_mean_creator.make_dict(),
                lai_std_creator.make_dict(),
                lai_trend_creator.make_dict(),
                nee_mean_creator.make_dict(),
                nee_std_creator.make_dict(),
                nee_trend_creator.make_dict(),
                nbp_mean_creator.make_dict(),
                nbp_std_creator.make_dict(),
                nbp_trend_creator.make_dict(),
                ffire_mean_creator.make_dict(),
                ffire_std_creator.make_dict(),
                ffire_trend_creator.make_dict(),
            ]
        )

        # -- 5.2: Colorbar settings for data over 'Europe', 'NH' regions:
        # -- Burned area properties:
        ba_mean_creator = Map_settings( 'burned_area', 'mean' ,  0.0 , 0.05, 'hot_r')
        ba_std_creator = Map_settings(  'burned_area', 'std'  ,  0.0 , 0.03, 'hot_r')
        ba_trend_creator = Map_settings('burned_area', 'trend', -1e-4, 1e-4, 'RdBu_r')
        # -- cVeg properties:
        cveg_mean_creator = Map_settings( 'cVeg', 'mean' ,  0.0 , 10.0 , 'gist_earth_r')
        cveg_std_creator = Map_settings(  'cVeg', 'std'  ,  0.0 ,  1.5 , 'gist_earth_r')
        cveg_trend_creator = Map_settings('cVeg', 'trend', -0.04,  0.04, 'RdBu_r')
        # -- GPP properties (Gross Primary Production):
        gpp_mean_creator = Map_settings( 'gpp', 'mean' ,   0.0, 3000.0, 'gist_earth_r')
        gpp_std_creator = Map_settings(  'gpp', 'std'  ,   0.0,  300.0, 'gist_earth_r')
        gpp_trend_creator = Map_settings('gpp', 'trend', -10.0,   10.0, 'RdBu_r')
        # -- NPP properties (Net primary production):
        npp_mean_creator = Map_settings( 'npp', 'mean' ,  0.0, 1500.0, 'gist_earth_r')
        npp_std_creator = Map_settings(  'npp', 'std'  ,  0.0,  200.0, 'gist_earth_r')
        npp_trend_creator = Map_settings('npp', 'trend', -6.0,    6.0, 'RdBu_r')
        # -- LAI properties (Leaf Area Index):
        lai_mean_creator = Map_settings( 'lai', 'mean' ,  0.0 , 6.0 , 'Greens')
        lai_std_creator = Map_settings(  'lai', 'std'  ,  0.0 , 3.0 , 'Greens')
        lai_trend_creator = Map_settings('lai', 'trend', -0.03, 0.03, 'PRGn')
        # -- NEE properties (Net Ecosystem Exchange):
        nee_mean_creator = Map_settings( 'nee', 'mean' , -100.0,  50.0, 'PRGn')
        nee_std_creator = Map_settings(  'nee', 'std'  ,    0.0, 100.0, 'Greens')
        nee_trend_creator = Map_settings('nee', 'trend',   -2.0,   2.0, 'RdBu_r')
        # -- NPB properties (Net Biome Production):
        nbp_mean_creator = Map_settings( 'nbp', 'mean' , -60.0, 60.0, 'PRGn')
        nbp_std_creator = Map_settings(  'nbp', 'std'  ,   0.0,100.0, 'Greens')
        nbp_trend_creator = Map_settings('nbp', 'trend',  -2.0,  2.0, 'RdBu_r')
        # -- fFire properties (CO2 Flux to Atmosphere from Fire):
        ffire_mean_creator = Map_settings( 'fFire', 'mean' ,  0.0, 10.0, 'hot_r')
        ffire_std_creator = Map_settings(  'fFire', 'std'  ,  0.0, 10.0, 'hot_r')
        ffire_trend_creator = Map_settings('fFire', 'trend', -0.1,  0.1, 'RdBu_r')
        # -- Create list of settings:
        cfg.add(
            'clb_limits_EN', [
                ba_mean_creator.make_dict(),
                ba_std_creator.make_dict(),
                ba_trend_creator.make_dict(),
                cveg_mean_creator.make_dict(),
                cveg_std_creator.make_dict(),
                cveg_trend_creator.make_dict(),
                gpp_mean_creator.make_dict(),
                gpp_std_creator.make_dict(),
                gpp_trend_creator.make_dict(),
                npp_mean_creator.make_dict(),
                npp_std_creator.make_dict(),
                npp_trend_creator.make_dict(),
                lai_mean_creator.make_dict(),
                lai_std_creator.make_dict(),
                lai_trend_creator.make_dict(),
                nee_mean_creator.make_dict(),
                nee_std_creator.make_dict(),
                nee_trend_creator.make_dict(),
                nbp_mean_creator.make_dict(),
                nbp_std_creator.make_dict(),
                nbp_trend_creator.make_dict(),
                ffire_mean_creator.make_dict(),
                ffire_std_creator.make_dict(),
                ffire_trend_creator.make_dict(),
            ]
        )

        # Section 6: 2D plots settings (limits for axis):
        # =====================================================================
        #  Settings for 2D plots (difference mode):
        # Actual matplotlib colormap are here:
        #    https://matplotlib.org/stable/tutorials/colors/colormaps.html
        
        # -- 6.1: Colorbar settings for data over 'Global', 'Tropics', 'Other' regions
        # -- Burned area properties:
        ba_mean_creator = Map_settings( 'burned_area', 'mean' , -0.001, 0.001, 'RdBu_r')
        ba_std_creator = Map_settings(  'burned_area', 'std'  , -0.03 , 0.03 , 'RdBu_r')
        ba_trend_creator = Map_settings('burned_area', 'trend', -1e-4 , 1e-4 , 'bwr')
        # -- cVeg properties:
        cveg_mean_creator = Map_settings( 'cVeg', 'mean' , -1.0 ,  1.0, 'PiYG')
        cveg_std_creator = Map_settings(  'cVeg', 'std'  , -0.6 ,  0.6, 'PiYG')
        cveg_trend_creator = Map_settings('cVeg', 'trend', -1e-3, 1e-3, 'PiYG')
        # -- GPP properties (Gross Primary Production):
        gpp_mean_creator = Map_settings( 'gpp', 'mean' , -40.0, 40.0, 'PiYG')
        gpp_std_creator = Map_settings(  'gpp', 'std'  , -20.0, 20.0, 'PiYG')
        gpp_trend_creator = Map_settings('gpp', 'trend',  -0.4,  0.4, 'PiYG')
        # -- NPP properties (Net primary production):
        npp_mean_creator = Map_settings( 'npp', 'mean' , -20.0, 20.0, 'PiYG')
        npp_std_creator = Map_settings(  'npp', 'std'  , -15.0, 15.0, 'PiYG')
        npp_trend_creator = Map_settings('npp', 'trend',  -0.4,  0.4, 'PiYG')
        # -- LAI properties (Leaf Area Index):
        lai_mean_creator = Map_settings( 'lai', 'mean' , -1.0 ,  1.0, 'PiYG')
        lai_std_creator = Map_settings(  'lai', 'std'  , -0.4 ,  0.4, 'PiYG')
        lai_trend_creator = Map_settings('lai', 'trend', -1e-3, 1e-3, 'PiYG')
        # -- NEE properties (Net Ecosystem Exchange):
        nee_mean_creator = Map_settings( 'nee', 'mean' , -30.0, 30.0, 'PiYG')
        nee_std_creator = Map_settings(  'nee', 'std'  , -30.0, 30.0, 'PiYG')
        nee_trend_creator = Map_settings('nee', 'trend',  -0.5,  0.5, 'PiYG')
        # -- NPB properties (Net Biome Production):
        nbp_mean_creator = Map_settings( 'nbp', 'mean' , -30.0, 30.0, 'PiYG')
        nbp_std_creator = Map_settings(  'nbp', 'std'  , -30.0, 30.0, 'PiYG')
        nbp_trend_creator = Map_settings('nbp', 'trend',  -0.4,  0.4, 'PiYG')
        # -- fFire properties (CO2 Flux to Atmosphere from Fire):
        ffire_mean_creator = Map_settings( 'fFire', 'mean' , -10.0, 10.0, 'PiYG')
        ffire_std_creator = Map_settings(  'fFire', 'std'  ,  -6.0,  6.0, 'PiYG')
        ffire_trend_creator = Map_settings('fFire', 'trend',  -0.2,  0.2, 'PiYG')

        # -- Create list of settings:
        cfg.add(
            'clb_diff_limits_GTO', [
                ba_mean_creator.make_dict(),
                ba_std_creator.make_dict(),
                ba_trend_creator.make_dict(),
                cveg_mean_creator.make_dict(),
                cveg_std_creator.make_dict(),
                cveg_trend_creator.make_dict(),
                gpp_mean_creator.make_dict(),
                gpp_std_creator.make_dict(),
                gpp_trend_creator.make_dict(),
                npp_mean_creator.make_dict(),
                npp_std_creator.make_dict(),
                npp_trend_creator.make_dict(),
                lai_mean_creator.make_dict(),
                lai_std_creator.make_dict(),
                lai_trend_creator.make_dict(),
                nee_mean_creator.make_dict(),
                nee_std_creator.make_dict(),
                nee_trend_creator.make_dict(),
                nbp_mean_creator.make_dict(),
                nbp_std_creator.make_dict(),
                nbp_trend_creator.make_dict(),
                ffire_mean_creator.make_dict(),
                ffire_std_creator.make_dict(),
                ffire_trend_creator.make_dict(),
            ]
        )

        # -- 6.2: Colorbar settings for data over 'Europe', 'NH' regions
        # -- Burned area properties:
        ba_mean_creator = Map_settings( 'burned_area', 'mean' , -0.05, 0.05, 'RdBu_r')
        ba_std_creator = Map_settings(  'burned_area', 'std'  , -0.03, 0.03, 'RdBu_r')
        ba_trend_creator = Map_settings('burned_area', 'trend', -1e-3, 1e-3, 'bwr')
        # -- cVeg properties:
        cveg_mean_creator = Map_settings( 'cVeg', 'mean' , -0.4,  0.4, 'PiYG')
        cveg_std_creator = Map_settings(  'cVeg', 'std'  , -0.2,  0.2, 'PiYG')
        cveg_trend_creator = Map_settings('cVeg', 'trend', 1e-3, 1e-3, 'PiYG')
        # -- GPP properties (Gross Primary Production):
        gpp_mean_creator = Map_settings( 'gpp', 'mean' , -40.0, 40.0, 'PiYG')
        gpp_std_creator = Map_settings(  'gpp', 'std'  , -20.0, 20.0, 'PiYG')
        gpp_trend_creator = Map_settings('gpp', 'trend',  -0.4,  0.4, 'PiYG')
        # -- NPP properties (Net primary production):
        npp_mean_creator = Map_settings( 'npp', 'mean' , -20.0, 20.0, 'PiYG')
        npp_std_creator = Map_settings(  'npp', 'std'  , -15.0, 15.0, 'PiYG')
        npp_trend_creator = Map_settings('npp', 'trend',  -0.4,  0.4, 'PiYG')
        # -- LAI properties (Leaf Area Index):
        lai_mean_creator = Map_settings( 'lai', 'mean' , -2.0 ,  2.0, 'PiYG')
        lai_std_creator = Map_settings(  'lai', 'std'  , -0.4 ,  0.4, 'PiYG')
        lai_trend_creator = Map_settings('lai', 'trend', -1e-2, 1e-2, 'PiYG')
        # -- NEE properties (Net Ecosystem Exchange):
        nee_mean_creator = Map_settings( 'nee', 'mean' , -7.5, 7.5, 'PiYG')
        nee_std_creator = Map_settings(  'nee', 'std'  , -7.5, 7.5, 'PiYG')
        nee_trend_creator = Map_settings('nee', 'trend', -0.4, 0.4, 'PiYG')
        # -- NPB properties (Net Biome Production):
        nbp_mean_creator = Map_settings( 'nbp', 'mean' , -7.5, 7.5, 'PiYG')
        nbp_std_creator = Map_settings(  'nbp', 'std'  , -7.5, 7.5, 'PiYG')
        nbp_trend_creator = Map_settings('nbp', 'trend', -0.4, 0.4, 'PiYG')
        # -- fFire properties (CO2 Flux to Atmosphere from Fire):
        ffire_mean_creator = Map_settings( 'fFire', 'mean' , -4.0, 4.0, 'PiYG')
        ffire_std_creator = Map_settings(  'fFire', 'std'  , -2.0, 2.0, 'PiYG')
        ffire_trend_creator = Map_settings('fFire', 'trend', -0.1, 0.1, 'PiYG')
        # -- Create list of settings:
        cfg.add(
            'clb_diff_limits_EN', [
                ba_mean_creator.make_dict(),
                ba_std_creator.make_dict(),
                ba_trend_creator.make_dict(),
                cveg_mean_creator.make_dict(),
                cveg_std_creator.make_dict(),
                cveg_trend_creator.make_dict(),
                gpp_mean_creator.make_dict(),
                gpp_std_creator.make_dict(),
                gpp_trend_creator.make_dict(),
                npp_mean_creator.make_dict(),
                npp_std_creator.make_dict(),
                npp_trend_creator.make_dict(),
                lai_mean_creator.make_dict(),
                lai_std_creator.make_dict(),
                lai_trend_creator.make_dict(),
                nee_mean_creator.make_dict(),
                nee_std_creator.make_dict(),
                nee_trend_creator.make_dict(),
                nbp_mean_creator.make_dict(),
                nbp_std_creator.make_dict(),
                nbp_trend_creator.make_dict(),
                ffire_mean_creator.make_dict(),
                ffire_std_creator.make_dict(),
                ffire_trend_creator.make_dict(),
            ]
        )

        # Section 7: Settings for subplots
        # ======================================================================
        
        # -- 7.1: Special settings for subplots positions
        # User Settings for positions of subplots in the figure depending on 
        # projection. This parameters are using in function collage_plot 
        # from vis_module. NBC - I used this abbreviation for this phrase
        #     --> number of columns in one row
        
        # -- 7.1: Settings for 2D plot:
        # -- Region ---> Global. Type projection ---> 'moll' 
        cfg.add(
            'layout_settings_moll', {
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
        )
        # -- 7.2: Settings for 2D plot:
        # Region ---> Europe, Other. Type projection ---> 'merc' 
        cfg.add(
            'layout_settings_merc', {
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
        )
        # -- 7.3: Settings for 2D plot:
        # Region ---> Tropics, NH. Type projection ---> 'cyl' 
        cfg.add(
            'layout_settings_cyl', {
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
        )

        # Section 8: Settings for RECCAP2 domains:
        # ======================================================================
        # -- User settings for burned area:
        ba_min = 0.0
        ba_max1,  ba_max2,  ba_max3,  ba_max4,  ba_max5  =  50.1, 200.1, 600.1, 2000.1, 3000.1
        ba_step1, ba_step2, ba_step3, ba_step4, ba_step5 =   5.0,  20.0,  60.0,  200.0,  300.0
        # -- User settings for cVeg:
        cv_min = 0.0
        cv_max1,  cv_max2,  cv_max3,  cv_max4  = 10.1, 25.1, 50.1, 125.1
        cv_step1, cv_step2, cv_step3, cv_step4 =  1.0,  2.5,  5.0,  12.5
        # -- User settings for GPP:
        gp_min = 0.0
        gp_max1,  gp_max2,  gp_max3,  gp_max4  = 5.1, 10.1, 20.1, 30.1
        gp_step1, gp_step2, gp_step3, gp_step4 = 0.5,  1.0,  2.0,  3.0
        # -- User settings for NPP:
        np_min = 0.0
        np_max1,  np_max2,  np_max3,  np_max4  = 2.1, 5.1, 10.1, 15.1
        np_step1, np_step2, np_step3, np_step4 = 0.2, 0.5,  1.0,  1.5
        # -- User settings for NBP:
        nb_min1, nb_max1, nb_step1 = -1.8, 1.81, 0.2
        # -- User settings for NEE:
        ne_min1, ne_max1, ne_step1 = -1.4, 0.81, 0.2
        ne_min2, ne_max2, ne_step2 = -1.2, 0.21, 0.2
        ne_min3, ne_max3, ne_step3 = -0.8, 0.41, 0.2
        ne_min4, ne_max4, ne_step4 = -0.2, 0.21, 0.1
        # -- User settings for LAI:
        la_min1, la_max1, la_step1 = 0.0, 2.6 , 0.2
        la_min2, la_max2, la_step2 = 0.0, 5.1 , 0.5
        la_min3, la_max3, la_step3 = 0.0, 6.1 , 0.5
        
        # -- User settings for fFire:
        ff_min = 0.0
        ff_max1,  ff_max2,  ff_max3,  ff_max4  = 0.101, 0.21, 0.51, 1.51
        ff_step1, ff_step2, ff_step3, ff_step4 = 0.01 , 0.02, 0.05, 0.15
               
        # -- User limits for Y axis:
        cfg.add(
            'limits4reccap2_domains', {
                'burned_area' : {
                    'USA'                     : [ ba_min, ba_max3, ba_step3],
                    'Canada'                  : [ ba_min, ba_max2, ba_step2],
                    'Central_America'         : [ ba_min, ba_max3, ba_step3],
                    'Northern_South_America'  : [ ba_min, ba_max2, ba_step2],
                    'Brazil'                  : [ ba_min, ba_max4, ba_step4],
                    'Southwest_South_America' : [ ba_min, ba_max3, ba_step3],
                    'Europe'                  : [ ba_min, ba_max2, ba_step2],
                    'Northern_Africa'         : [ ba_min, ba_max5, ba_step5],
                    'Equatorial_Africa'       : [ ba_min, ba_max4, ba_step4],
                    'Southern_Africa'         : [ ba_min, ba_max5, ba_step5],
                    'Russia'                  : [ ba_min, ba_max3, ba_step3],
                    'Central_Asia'            : [ ba_min, ba_max3, ba_step3],
                    'Mideast'                 : [ ba_min, ba_max3, ba_step3],
                    'China'                   : [ ba_min, ba_max2, ba_step2],
                    'Korea_and_Japan'         : [ ba_min, ba_max1, ba_step1],
                    'South_Asia'              : [ ba_min, ba_max3, ba_step3],
                    'Southeast_Asia'          : [ ba_min, ba_max2, ba_step2],
                    'Oceania'                 : [ ba_min, ba_max5, ba_step5],
                },
                'cVeg' : {
                    'USA'                     : [ cv_min, cv_max3, cv_step3],
                    'Canada'                  : [ cv_min, cv_max3, cv_step3],
                    'Central_America'         : [ cv_min, cv_max2, cv_step2],
                    'Northern_South_America'  : [ cv_min, cv_max3, cv_step3],
                    'Brazil'                  : [ cv_min, cv_max4, cv_step4],
                    'Southwest_South_America' : [ cv_min, cv_max3, cv_step3],
                    'Europe'                  : [ cv_min, cv_max3, cv_step3],
                    'Northern_Africa'         : [ cv_min, cv_max1, cv_step1],
                    'Equatorial_Africa'       : [ cv_min, cv_max4, cv_step4],
                    'Southern_Africa'         : [ cv_min, cv_max2, cv_step2],
                    'Russia'                  : [ cv_min, cv_max4, cv_step4],
                    'Central_Asia'            : [ cv_min, cv_max1, cv_step1],
                    'Mideast'                 : [ cv_min, cv_max1, cv_step1],
                    'China'                   : [ cv_min, cv_max3, cv_step3],
                    'Korea_and_Japan'         : [ cv_min, cv_max1, cv_step1],
                    'South_Asia'              : [ cv_min, cv_max2, cv_step2],
                    'Southeast_Asia'          : [ cv_min, cv_max4, cv_step4],
                    'Oceania'                 : [ cv_min, cv_max2, cv_step2],
                },
                'lai' : {
                    'USA'                     : [ la_min2, la_max2, la_step2],
                    'Canada'                  : [ la_min3, la_max3, la_step3],
                    'Central_America'         : [ la_min2, la_max2, la_step2],
                    'Northern_South_America'  : [ la_min3, la_max3, la_step3],
                    'Brazil'                  : [ la_min3, la_max3, la_step3],
                    'Southwest_South_America' : [ la_min2, la_max2, la_step2],
                    'Europe'                  : [ la_min2, la_max2, la_step2],
                    'Northern_Africa'         : [ la_min1, la_max1, la_step1],
                    'Equatorial_Africa'       : [ la_min2, la_max2, la_step2],
                    'Southern_Africa'         : [ la_min2, la_max2, la_step2],
                    'Russia'                  : [ la_min2, la_max2, la_step2],
                    'Central_Asia'            : [ la_min1, la_max1, la_step1],
                    'Mideast'                 : [ la_min1, la_max1, la_step1],
                    'China'                   : [ la_min2, la_max2, la_step2],
                    'Korea_and_Japan'         : [ la_min2, la_max2, la_step2],
                    'South_Asia'              : [ la_min2, la_max2, la_step2],
                    'Southeast_Asia'          : [ la_min3, la_max3, la_step3],
                    'Oceania'                 : [ la_min1, la_max1, la_step1],
                },
                'gpp' : {
                    'USA'                     : [ gp_min, gp_max3, gp_step3],
                    'Canada'                  : [ gp_min, gp_max2, gp_step2],
                    'Central_America'         : [ gp_min, gp_max2, gp_step2],
                    'Northern_South_America'  : [ gp_min, gp_max2, gp_step2],
                    'Brazil'                  : [ gp_min, gp_max4, gp_step4],
                    'Southwest_South_America' : [ gp_min, gp_max3, gp_step3],
                    'Europe'                  : [ gp_min, gp_max2, gp_step2],
                    'Northern_Africa'         : [ gp_min, gp_max2, gp_step2],
                    'Equatorial_Africa'       : [ gp_min, gp_max3, gp_step3],
                    'Southern_Africa'         : [ gp_min, gp_max2, gp_step2],
                    'Russia'                  : [ gp_min, gp_max3, gp_step3],
                    'Central_Asia'            : [ gp_min, gp_max1, gp_step1],
                    'Mideast'                 : [ gp_min, gp_max1, gp_step1],
                    'China'                   : [ gp_min, gp_max3, gp_step3],
                    'Korea_and_Japan'         : [ gp_min, gp_max1, gp_step1],
                    'South_Asia'              : [ gp_min, gp_max2, gp_step2],
                    'Southeast_Asia'          : [ gp_min, gp_max3, gp_step3],
                    'Oceania'                 : [ gp_min, gp_max2, gp_step2],
                },
                'npp' : {
                    'USA'                     : [ np_min, np_max3, np_step3],
                    'Canada'                  : [ np_min, np_max2, np_step2],
                    'Central_America'         : [ np_min, np_max2, np_step2],
                    'Northern_South_America'  : [ np_min, np_max2, np_step2],
                    'Brazil'                  : [ np_min, np_max4, np_step4],
                    'Southwest_South_America' : [ np_min, np_max3, np_step3],
                    'Europe'                  : [ np_min, np_max2, np_step2],
                    'Northern_Africa'         : [ np_min, np_max2, np_step2],
                    'Equatorial_Africa'       : [ np_min, np_max3, np_step3],
                    'Southern_Africa'         : [ np_min, np_max2, np_step2],
                    'Russia'                  : [ np_min, np_max3, np_step3],
                    'Central_Asia'            : [ np_min, np_max2, np_step2],
                    'Mideast'                 : [ np_min, np_max1, np_step1],
                    'China'                   : [ np_min, np_max3, np_step3],
                    'Korea_and_Japan'         : [ np_min, np_max1, np_step1],
                    'South_Asia'              : [ np_min, np_max2, np_step2],
                    'Southeast_Asia'          : [ np_min, np_max3, np_step3],
                    'Oceania'                 : [ np_min, np_max2, np_step2],
                },
                'nee' : {
                    'USA'                     : [ne_min2, ne_max2, ne_step2],
                    'Canada'                  : [ne_min3, ne_max3, ne_step3],
                    'Central_America'         : [ne_min3, ne_max3, ne_step3],
                    'Northern_South_America'  : [ne_min3, ne_max3, ne_step3],
                    'Brazil'                  : [ne_min1, ne_max1, ne_step1],
                    'Southwest_South_America' : [ne_min3, ne_max3, ne_step3],
                    'Europe'                  : [ne_min3, ne_max3, ne_step3],
                    'Northern_Africa'         : [ne_min3, ne_max3, ne_step3],
                    'Equatorial_Africa'       : [ne_min3, ne_max3, ne_step3],
                    'Southern_Africa'         : [ne_min3, ne_max3, ne_step3],
                    'Russia'                  : [ne_min2, ne_max2, ne_step2],
                    'Central_Asia'            : [ne_min3, ne_max3, ne_step3],
                    'Mideast'                 : [ne_min4, ne_max4, ne_step4],
                    'China'                   : [ne_min3, ne_max3, ne_step3],
                    'Korea_and_Japan'         : [ne_min4, ne_max4, ne_step4],
                    'South_Asia'              : [ne_min3, ne_max3, ne_step3],
                    'Southeast_Asia'          : [ne_min3, ne_max3, ne_step3],
                    'Oceania'                 : [ne_min1, ne_max1, ne_step1],
                },
                'nbp' : {
                    'USA'                     : [nb_min1, nb_max1, nb_step1],
                    'Canada'                  : [nb_min1, nb_max1, nb_step1],
                    'Central_America'         : [nb_min1, nb_max1, nb_step1],
                    'Northern_South_America'  : [nb_min1, nb_max1, nb_step1],
                    'Brazil'                  : [nb_min1, nb_max1, nb_step1],
                    'Southwest_South_America' : [nb_min1, nb_max1, nb_step1],
                    'Europe'                  : [nb_min1, nb_max1, nb_step1],
                    'Northern_Africa'         : [nb_min1, nb_max1, nb_step1],
                    'Equatorial_Africa'       : [nb_min1, nb_max1, nb_step1],
                    'Southern_Africa'         : [nb_min1, nb_max1, nb_step1],
                    'Russia'                  : [nb_min1, nb_max1, nb_step1],
                    'Central_Asia'            : [nb_min1, nb_max1, nb_step1],
                    'Mideast'                 : [nb_min1, nb_max1, nb_step1],
                    'China'                   : [nb_min1, nb_max1, nb_step1],
                    'Korea_and_Japan'         : [nb_min1, nb_max1, nb_step1],
                    'South_Asia'              : [nb_min1, nb_max1, nb_step1],
                    'Southeast_Asia'          : [nb_min1, nb_max1, nb_step1],
                    'Oceania'                 : [nb_min1, nb_max1, nb_step1],
                },
                'fFire' : {
                    'USA'                     : [ ff_min, ff_max3, ff_step3],
                    'Canada'                  : [ ff_min, ff_max2, ff_step2],
                    'Central_America'         : [ ff_min, ff_max3, ff_step3],
                    'Northern_South_America'  : [ ff_min, ff_max2, ff_step2],
                    'Brazil'                  : [ ff_min, ff_max4, ff_step4],
                    'Southwest_South_America' : [ ff_min, ff_max3, ff_step3],
                    'Europe'                  : [ ff_min, ff_max1, ff_step1],
                    'Northern_Africa'         : [ ff_min, ff_max3, ff_step3],
                    'Equatorial_Africa'       : [ ff_min, ff_max4, ff_step4],
                    'Southern_Africa'         : [ ff_min, ff_max4, ff_step4],
                    'Russia'                  : [ ff_min, ff_max3, ff_step3],
                    'Central_Asia'            : [ ff_min, ff_max2, ff_step2],
                    'Mideast'                 : [ ff_min, ff_max1, ff_step1],
                    'China'                   : [ ff_min, ff_max2, ff_step2],
                    'Korea_and_Japan'         : [ ff_min, ff_max1, ff_step1],
                    'South_Asia'              : [ ff_min, ff_max3, ff_step3],
                    'Southeast_Asia'          : [ ff_min, ff_max3, ff_step3],
                    'Oceania'                 : [ ff_min, ff_max3, ff_step3],
                },
            }
        )

        # Section 9: User settings for linear plots (color, style, hatches)
        # ======================================================================
        # -- 9.1: Colors for research simulations and datasets:
        cfg.add(
            'xfire_colors', {
                # Simulation          color    style
                # OCN simulations based on RECCAP_v1 experiment (prepared by Ana):
                'OCN_S2.1'     : ['peru'   , '-' , '++++' ],
                'OCN_S2.2'     : ['peru'   , '--', '----' ],
                'OCN_S2.1_nf'  : ['peru'   , '-.', 'xxxx' ],
                'OCN_S2.1.1'   : ['peru'   , ':' , '\\\\' ],
                'OCN_S3.1'     : ['brown'  , '-' , '****' ],
                'OCN_S3.2'     : ['brown'  , '--', 'oooo' ],
                'OCN_S3.1_nf'  : ['brown'  , '-.', '++++' ],
                # OCN simulations based on v202209 experiment (prepared by Evgenii):
                'OCN_S0'       : ['tomato' , ':' , '++++' ],
                'OCN_S2Prog'   : ['tomato' , '-' , '////' ],
                'OCN_S2Diag'   : ['tomato' , '--', ''     ],
                # OCN simulations based on v202302 experiment (prepared by Evgenii):
                'OCN_Spost_v3' : ['maroon' , '-.', '++++' ],
                'OCN_S0_v3'    : ['maroon' , ':' , '----' ],
                'OCN_S2Prog_v3': ['maroon' , '-' , '////' ],
                'OCN_S2Diag_v3': ['maroon' , '--', ''     ],
                # OCN simulations based on v202302 experiment (prepared by Evgenii):
                'OCN_Spost_v4' : ['red'    , '-.', '++++' ],
                'OCN_S0_v4'    : ['red'    , ':' , '----' ],
                'OCN_S2Prog_v4': ['red'    , '-' , '////' ],
                'OCN_S2Diag_v4': ['coral'  , '--', ''     ],
                # Colors for satellite datasets with fire and fFire
                'BA_MODIS'     : ['black'  , '-' , ''     ],
                'BA_AVHRR'     : ['black'  , ':' , '////' ],
                'GFED4.1s'     : ['grey'  , '--', '....'  ],
                'GFED_TOT'     : ['grey'  , '-.', '\\\\'  ],
                'GFED_FL'      : ['black'  , '-' , ''     ],
                'GFED_AG_TOT'  : ['black'  , '-.', '||||' ],
                'GFED_BG_TOT'  : ['black'  , ':' , '||||' ],
                'GFED_AG_FL'   : ['black'  , '-.', ''     ],
                'GFED_BG_FL'   : ['black'  , ':' , ''     ],
                # Colors for JULES simulations
                'JUL_S0'       : ['blue'   , ':' , '----' ],
                'JUL_S2Prog'   : ['blue'   , '-' , '////' ],
                'JUL_S2Diag'   : ['blue'   , '--', ''     ],
                # Colors for ORCHIDEE simulations
                'ORC_S0'       : ['green'  , ':' , '----' ],
                'ORC_S2Prog'   : ['green'  , '-' , '////' ],
                'ORC_S2Diag'   : ['green'  , '--', ''     ],
                # Colors for satellite datasets with GPP and NPP
                'MOD17A2HGFv061' : ['black'  , '-' , ''     ],
                'MOD17A3HGFv061' : ['grey'   , '-.', ''     ],
                # Colors for satellite datasets with LAI
                'LAI_LTDR'     : ['black'  , '-' , ''     ],
                'LAI_MODIS'    : ['grey'   , ':' , ''     ],
                'GLOBMAP'      : ['grey'  , '--', '||||' ],
                'NDEP'         : ['blue'   , '-' , ''     ],
            }
        )

        # -- 9.2: Linear plots for check_ocn_pft script:
        cfg.add(
            'check_colors', {
                # line number, parameter, relevant values
                # Settings for 2 lines:
                2   : {'color' : ['orangered',           'black'         ],
                       'style' : [   '-'     ,             '-'           ]},
                # Settings for 3 lines (BS + CROPS and Grass + Srubs)
                3  : {'color'  : ['orangered',           'black', 'black'],
                      'style'  : [    '-'    ,             '-'  ,   '-.' ]},
                # Settings for 4 lines (evergreen and deciduous trees)
                4  : {'color'  : ['orangered', 'tomato', 'black', 'black'],
                      'style'  : [    '-'    ,   '-.'  ,   '-'  ,   '-.' ]},
            }
        )

        # -- 9.3: Linear plots for landcover script:
        cfg.add(
            'ln_colors', {
                'OCN' : {
                #    PFT      color       style
                    'BS'  : ['blue'      ,  '-' ],
                    'TrBE': ['orange'    ,  '-' ],
                    'TrBR': ['brown'     ,  '-' ],
                    'TeNE': ['darkorchid',  '-' ],
                    'TeBE': ['orange'    ,  '--'],
                    'TeBS': ['brown'     ,  '-.'],
                    'BNE' : ['darkorchid',  '-.'],
                    'BBS' : ['brown'     ,  '--'],
                    'BNS' : ['lawngreen' ,  '-' ],
                    'HC3' : ['green'     ,  '-' ],
                    'HC4' : ['green'     ,  '--'],
                    'CC3' : ['blue'      ,  ':' ],
                    'CC4' : ['blue'      ,  '--']}
            }
        )

        # Section 10: User settings for PFT:
        # ======================================================================
        # -- 10.1: OCN PFT:
        cfg.add(
            'ocn_pft', [
                {'index' : 0 , 'veg_type' :  1, 'PFT' : 'BS'  , 'fname' : 'Bare soil'                        }, # 'natural'
                {'index' : 1 , 'veg_type' :  2, 'PFT' : 'TrBE', 'fname' : 'tropical broadleaved evergreen'   }, # 'natural'
                {'index' : 2 , 'veg_type' :  3, 'PFT' : 'TrBR', 'fname' : 'tropical broadleaved raingreen'   }, # 'natural'
                {'index' : 3 , 'veg_type' :  4, 'PFT' : 'TeNE', 'fname' : 'temperate needleleaved evergreen' }, # 'natural'
                {'index' : 4 , 'veg_type' :  5, 'PFT' : 'TeBE', 'fname' : 'temperate broadleaved evergreen'  }, # 'natural'
                {'index' : 5 , 'veg_type' :  6, 'PFT' : 'TeBS', 'fname' : 'temperate broadleaved summergreen'}, # 'natural'
                {'index' : 6 , 'veg_type' :  7, 'PFT' : 'BNE' , 'fname' : 'boreal needleleaved evergreen'    }, # 'natural'
                {'index' : 7 , 'veg_type' :  8, 'PFT' : 'BBS' , 'fname' : 'boreal broadleaved summergreen'   }, # 'natural'
                {'index' : 8 , 'veg_type' :  9, 'PFT' : 'BNS' , 'fname' : 'boreal needlleaved summergreen'   }, # 'natural'
                {'index' : 9 , 'veg_type' : 10, 'PFT' : 'HC3' , 'fname' : 'C3 grass'                         }, # 'natural'
                {'index' : 10, 'veg_type' : 11, 'PFT' : 'HC4' , 'fname' : 'C4 grass'                         }, # 'natural'
                {'index' : 11, 'veg_type' : 12, 'PFT' : 'CC3' , 'fname' : 'C3 agriculture'                   }, # 'crops'
                {'index' : 12, 'veg_type' : 13, 'PFT' : 'CC4' , 'fname' : 'C4 agriculture'                   }, # 'crops'
            ]
        )
        # -- 10.2: ESA-CCI MODIS v5.0 PFT:
        # Information for LandCover Class Table is located at
        # https://developers.google.com/earth-engine/datasets/catalog/ESA_CCI_FireCCI_5_1#bands
        cfg.add(
            'modis_pft', [
                {'index' :  0, 'value' :  10, 'color' : 'ffff64', 'veg_class' : 'Cropland, rainfed'                                               }, # 'crops'
                {'index' :  1, 'value' :  20, 'color' : 'aaf0f0', 'veg_class' : 'Cropland, irrigated\n or post-flooding'                          }, # 'crops'
                {'index' :  2, 'value' :  30, 'color' : 'dcf064', 'veg_class' : 'Mosaic cropland (>50%)\n / natural vegetation (<50%)'            }, # 'crops'
                {'index' :  3, 'value' :  40, 'color' : 'c8c864', 'veg_class' : 'Mosaic natural vegetation (>50%)\n / cropland (<50%)'            }, # 'natural'
                {'index' :  4, 'value' :  50, 'color' : '006400', 'veg_class' : 'Tree cover, broadleaved, \n evergreen, closed to open (>15%)'    }, # 'natural'
                {'index' :  5, 'value' :  60, 'color' : '00a000', 'veg_class' : 'Tree cover, broadleaved, \n deciduous, closed to open (>15%)'    }, # 'natural'
                {'index' :  6, 'value' :  70, 'color' : '003c00', 'veg_class' : 'Tree cover, needleleaved,\n evergreen, closed to open (>15%)'    }, # 'natural'
                {'index' :  7, 'value' :  80, 'color' : '285000', 'veg_class' : 'Tree cover, needleleaved,\n deciduous, closed to open (>15%)'    }, # 'natural'
                {'index' :  8, 'value' :  90, 'color' : '788200', 'veg_class' : 'Tree cover, mixed leaf type \n (broadleaved and needleleaved)'   }, # 'natural'
                {'index' :  9, 'value' : 100, 'color' : '8ca000', 'veg_class' : 'Mosaic tree and shrub (>50%)\n / herbaceous cover (<50%)'        }, # 'natural'
                {'index' : 10, 'value' : 110, 'color' : 'be9600', 'veg_class' : 'Mosaic herbaceous cover (>50%)\n / tree and shrub (<50%)'        }, # 'natural'
                {'index' : 11, 'value' : 120, 'color' : '966400', 'veg_class' : 'Shrubland'                                                       }, # 'natural'
                {'index' : 12, 'value' : 130, 'color' : 'ffb432', 'veg_class' : 'Grassland'                                                       }, # 'natural'
                {'index' : 13, 'value' : 140, 'color' : 'ffdcd2', 'veg_class' : 'Lichens and mosses'                                              }, # 'natural'
                {'index' : 14, 'value' : 150, 'color' : 'ffebaf', 'veg_class' : 'Sparse vegetation (tree, shrub,\n herbaceous cover) (<15%)'      }, # 'natural'
                {'index' : 15, 'value' : 160, 'color' : 'red'   , 'veg_class' : 'Tree cover, flooded, fresh or brackish water'                    }, # 'natural'
                {'index' : 16, 'value' : 170, 'color' : '009678', 'veg_class' : 'Tree cover, flooded,\n saline water'                             }, # 'natural'
                {'index' : 17, 'value' : 180, 'color' : '00dc82', 'veg_class' : 'Shrub or herbaceous cover,\n flooded, fresh/saline/brakish water'}, # 'natural'
            ]
        )
        return cfg

# -- Testing mode:
if __name__ == '__main__':
    bcc = Bulder_config_class()
    tlm = bcc.user_settings()
    print(tlm.get('clb_diff_limits_GTO'))
