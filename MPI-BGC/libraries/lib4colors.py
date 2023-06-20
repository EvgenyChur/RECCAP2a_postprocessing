# -*- coding: utf-8 -*-
"""
Module with user settings for linear plots depending on:
    1. xfire_colors -> type of model simulation;
    2. check_colors -> numbers of line for visualization;
    3. ln_colors    -> OCN PFT

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-11-10 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-15 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
           Added colors for landcover script
    1.3    2023-03-13 Evgenii Churiulin, MPI-BGC
           Added new colors for JULES and ORCHIDEE simulations 
    1.4    2023-03-20 Evgenii Churiulin, MPI-BGC
           Colors were updated
    1.5    2023-05-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ===================
# 1.1  Standard modules
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from libraries.lib4pft import ocn_pft

# ==========================   Colors and linestyles   ===================

# -- Linear plots for fire_xarray script:
# Colors for research simulations and datasets:
xfire_colors = {
    # Simulation          color    style
    # OCN simulations based on RECCAP_v1 experiment (prepared by Ana):
    'OCN_S2.1'       : ['peru'   , '-'  ],
    'OCN_S2.2'       : ['peru'   , '--' ],
    'OCN_S2.1_nf'    : ['peru'   , '-.' ],
    'OCN_S2.1.1'     : ['peru'   , ':'  ],
    'OCN_S3.1'       : ['brown'  , '-'  ],
    'OCN_S3.2'       : ['brown'  , '--' ],
    'OCN_S3.1_nf'    : ['brown'  , '-.' ],
    # OCN simulations based on v202209 experiment (prepared by Evgenii):
    'OCN_S0'         : ['tomato' , ':'  ],
    'OCN_S2Prog'     : ['tomato' , '-'  ],
    'OCN_S2Diag'     : ['tomato' , '--' ],
    # OCN simulations based on v202302 experiment (prepared by Evgenii):
    'OCN_Spost_v3'   : ['maroon' , '-.' ],
    'OCN_S0_v3'      : ['maroon' , ':'  ],
    'OCN_S2Prog_v3'  : ['maroon' , '-'  ],
    'OCN_S2Diag_v3'  : ['maroon' , '--' ],
    # Colors for satellite datasets with fire and fFire
    'BA_MODIS'       : ['black'  , '-'  ], 
    'BA_AVHRR'       : ['black'  , ':'  ],    
    'GFED4.1s'       : ['black'  , '--' ],
    'GFED_TOT'       : ['black'  , '-.' ],
    'GFED_FL'        : ['black'  , '-'  ],
    'GFED_AG_TOT'    : ['black'  , '-.' ],
    'GFED_BG_TOT'    : ['black'  , ':'  ],
    'GFED_AG_FL'     : ['black'  , '-.' ], 
    'GFED_BG_FL'     : ['black'  , ':'  ],
    # Colors for JULES simulations 
    'JUL_S0'         : ['blue'   , ':'  ],
    'JUL_S2Prog'     : ['blue'   , '-'  ],
    'JUL_S2Diag'     : ['blue'   , '--' ],
    # Colors for ORCHIDEE simulations
    'ORC_S0'         : ['green'  , ':'  ],
    'ORC_S2Prog'     : ['green'  , '-'  ],
    'ORC_S2Diag'     : ['green'  , '--' ],
    # Colors for satellite datasets with GPP and NPP
    'MOD17A2HGFv061' : ['black'  , '-'  ],
    'MOD17A3HGFv061' : ['black'  , '-.' ],
    # Colors for satellite datasets with LAI
    'LAI_LTDR'       : ['black'  , '-'  ],
    'LAI_MODIS'      : ['black'  , ':'  ],
    'GLOBMAP'        : ['black'  , '--' ],
    'NDEP'           : ['blue'   , '-'  ],
}

# -- Linear plots for check_ocn_pft script:
check_colors = {# line number, parameter, relevant values  
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

# -- Linear plots for landcover script:
ln_colors = {
    # Data type      PFT type      color       style
    'OCN'         : {'BS'    : ['blue'      ,  '-' ],
                     'TrBE'  : ['orange'    ,  '-' ],
                     'TrBR'  : ['brown'     ,  '-' ],
                     'TeNE'  : ['darkorchid',  '-' ],
                     'TeBE'  : ['orange'    ,  '--'],
                     'TeBS'  : ['brown'     ,  '-.'],
                     'BNE'   : ['darkorchid',  '-.'],
                     'BBS'   : ['brown'     ,  '--'],
                     'BNS'   : ['lawngreen' ,  '-' ],
                     'HC3'   : ['green'     ,  '-' ],
                     'HC4'   : ['green'     ,  '--'],
                     'CC3'   : ['blue'      ,  ':' ],
                     'CC4'   : ['blue'      ,  '--']}
}

colors_ocn = []
styles_ocn = []
for item in ocn_pft:
    colors_ocn.append(ln_colors.get('OCN').get(item['PFT'])[0])
    styles_ocn.append(ln_colors.get('OCN').get(item['PFT'])[1])
