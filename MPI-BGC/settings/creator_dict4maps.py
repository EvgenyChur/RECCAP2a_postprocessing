# -*- coding: utf-8 -*-
"""
Description: User class for creation correct user settings for 2D MAPs

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    08.11.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

class Map_settings:
    """User interface for controlling input user parameters for 2D maps:"""
    # -- Local variables:
    var_list = ['burned_area', 'cVeg', 'gpp', 'npp', 'lai', 'nee', 'nbp', 'fFire']
    stat_list = ['mean', 'std', 'trend']

    # -- Initialization:
    def __init__(
            self, var:str, stat_param:str, ymin:float, ymax: float, cbar:str):
        """Initialization of input parameters:"""
        # -- Call verify methods:
        self.verify_var(var)
        self.verify_stat_param(stat_param)
        # -- Set parameters:
        self.__var = var
        self.__stat_param = stat_param
        self.ymin = ymin
        self.ymax = ymax
        self.cbar = cbar

    # -- Control format of input variables:
    # -- 1.1: Verification of VAR parameter:
    @classmethod
    def verify_var(cls, var):
        # -- Check input format:
        if type(var) != str:
            raise TypeError('VAR variable should be a string')
        # -- Check type research parameter:
        if var not in cls.var_list:
            raise TypeError('There is no such research parameter')

    # -- 1.2: Verification of STAT_PARAM:
    @classmethod
    def verify_stat_param(cls, stat_param):
        # -- Check input format:
        if type(stat_param) != str:
            raise TypeError('STAT_PARAM variable should be a string')
        # -- Check type stat parameter:
        if stat_param not in cls.stat_list:
            raise TypeError('There is no such statistical parameter')

    # -- 1.3: Verification of YMIN:
    @classmethod
    def verify_ymin(cls, ymin):
        # -- Check input format:
        if type(ymin) != float:
            raise TypeError('YMIN variable should be a float or int')

    # -- 1.4: Verification of YMAX:
    @classmethod
    def verify_ymax(cls, ymax):
        # -- Check input format:
        if type(ymax) != float:
            raise TypeError('YMAX variable should be a float or int') 
    # -- 1.5: Verification of cbar:

    @classmethod
    def verify_cbar(cls, cbar):
        # -- Check input format:
        if type(cbar) != str:
            raise TypeError('CBAR variable should be a string')


    # -- Interection interfaces for work with input data:
    # -- 2.1: VAR Interface -> Cannot be changed from property object:
    @property
    def var(self):
        return self.__var

    # -- 2.2: STAT_PARAM Interface -> Cannot be changed from property object:
    @property
    def stat_param(self):
        return self.__stat_param

    # -- 2.3: YMIN Interface:
    @property
    def ymin(self):
        return self.__ymin

    @ymin.setter
    def ymin(self, ymin):
        self.verify_ymin(ymin)
        self.__ymin = ymin

    # -- 2.4: YMAX Interface:
    @property
    def ymax(self):
        return self.__ymax

    @ymax.setter
    def ymax(self, ymax):
        self.verify_ymax(ymax)
        self.__ymax = ymax

    # -- 2.5: CBAR Interface:
    @property
    def cbar(self):
        return self.__cbar

    @cbar.setter
    def cbar(self, cbar):
        self.verify_cbar(cbar)
        self.__cbar = cbar

    def make_dict(self):
        dict_var = {
            'mode' : self.var,
            'param': self.stat_param ,
            'ymin' : self.ymin,
            'ymax' : self.ymax,
            'cbar' : self.cbar,
        }
        return dict_var
