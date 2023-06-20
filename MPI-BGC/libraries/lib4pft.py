# -*- coding: utf-8 -*-

"""
Module with information about PFT settings for OCN, ESA-CCI MODIS:

If you want to use another PFT, please add metainformation of them into this
module

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-11-01 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2023-05-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# ===========================   PFT descriptions  ========================

# -- OCN PFT:
ocn_pft = [
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

# -- ESA-CCI MODISv5.0 PFT:
# 1. Information for LandCover Class Table is located at
# https://developers.google.com/earth-engine/datasets/catalog/ESA_CCI_FireCCI_5_1#bands
modis_pft = [
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
