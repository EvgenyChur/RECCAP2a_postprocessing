# -*- coding: utf-8 -*-
"""
Script for testing actual values of total burned area fraction based on ESA-CCI
data before OCN work and after. The results should be the same.

The data from OCN model is located into additional script (library)

Information about OCN PFT:
    pft  1: '          bared ground            ', 'natural'
    pft  2: 'tropical  broad-leaved evergreen  ', 'natural'
    pft  3: 'tropical  broad-leaved raingreen  ', 'natural' 
    pft  4: 'temperate needleleaf   evergreen  ', 'natural' 
    pft  5: 'temperate broad-leaved evergreen  ', 'natural' 
    pft  6: 'temperate broad-leaved summergreen', 'natural'
    pft  7: 'boreal    needleleaf   evergreen  ', 'natural'
    pft  8: 'boreal    broad-leaved summergreen', 'natural'
    pft  9: 'boreal    needleleaf   summergreen', 'natural' 
    pft 10: '          C3           grass      ', 'natural' 
    pft 11: '          C4           grass      ', 'natural' 
    pft 12: '          C3           agriculture', ' crops ' 
    pft 13: '          C4           agriculture', ' crops '

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-09-15 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
# -- Standard:
import sys
import numpy as np
# -- Personal:
import ocn_data4ctr_alg as oda
# =============================   Personal functions   ==================

# =============================   User settings   =======================

# -- Logical parameters:
# Do you want to test algorithm for 1 point?
lcal_point = False
# Do you want to test algorithm for grid (2D array)?
lcal_2D = True

# -- Main settings:
# Fire resistance for each PFT (got from OCN look up table):
resist = np.asarray(
    [0.0, 0.12, 0.50, 0.12, 0.50, 0.12, 0.12, 0.12, 0.12, 0.0, 0.0, 0.0, 0.0])

# -- Settings for 1 point:
if lcal_point is True:
    # -- Vegetation fraction in point by PFT (total = 1)
    veget_max =  np.asarray(
        [0.0, 0.0, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0, 0.3, 0.1, 0.1, 0.0, 0.0])
    # Select PFT from 2 - 11
    veget_max = veget_max[1 : -2]
    resist = resist[1 : -2]
    fire_BA = 0.5

# -- Settings for 2D arrays:
if lcal_2D is True:
    # -- Get OCN data (from log files):
    veget_max = oda.get_veget_max()
    m_tbaf, m_days, x_ocn, d_tbaf = oda.ocn_data()
    # -- Set of PFT index for OCN data
    pft_index = np.arange(0, 13, 1)

# =============================    Main program   =======================
if __name__ == '__main__':
    # -- Test calculations of burned area fraction for station:
    if lcal_point is True:
        # -- Quality control of veget_max data. should be <= 1:
        if np.round(veget_max.sum(),2) <= 1.0:
            print('veget_max values:', np.round(veget_max.sum(),2), '\n')
        else:
            print('Error: veget_max values > 1.0 \n')
            sys.exit()
        # -- Get X scale coefficient values:
        x_scale = 0.0
        for pft in range(len(resist)):
            x_scale += (1.0 - resist[pft]) * veget_max[pft]
        # -- Get BA for each PFT, except bare soil and crops:
        ba_pft =[]
        for pft in range(len(resist)):
            ba_pft.append((1 - resist[pft]) * fire_BA * veget_max[pft])
        # -- Control calculations:
        if np.asarray(ba_pft).sum() == fire_BA:
            print('There are no difference in fire fraction')
        else:
            ba_pft_new = []
            for pft in range(len(resist)):
                ba_pft_new.append(ba_pft[pft] / x_scale)
            print('ESA-CCI burned area fraction before new OCN algorithm: ', fire_BA)
            print(
                'ESA-CCI burned area fraction after  new OCN algorithm: ',
                np.round(np.asarray(ba_pft_new).sum(), 2)
            )

    # -- Test calculations of burned area fraction for 2D arrays:
    if lcal_2D is True:
        # -- Calculations of dayly values of burned area fraction per pixel:
        fire_frac = m_tbaf / m_days
        # -- Check veget_max --> should be less then 1:
        print('Check veget_max values for each pixel. Values should be <= 1: \n')
        tot_veget = veget_max.sum(axis = 1)
        for i in range(len(tot_veget)):
            if tot_veget[i] > 1.0:
                print('We have problems with veget_max values.')
                sys.exit()
        print('veget_max values are correct \n')
        # -- Get X parameter:
        x_scale = np.zeros(94)
        for i_pft in pft_index:
            if i_pft not in (0, 11, 12):
                for j in range(len(veget_max)):
                    x_scale[j] = x_scale[j] + (1 - resist[i_pft]) * veget_max[j,i_pft]
        # -- Calculation (burned area + fire resistance) / x_scale, except bare soil and crops:
        ba_pft = np.zeros((94, 13))
        for i_pft in pft_index:
            if i_pft not in (0, 11, 12):
                for j in range(len(veget_max)):
                    ba_pft[j, i_pft] = ((1 - resist[i_pft]) * fire_frac[j] * veget_max[j,i_pft]) / x_scale[j]
            else:
                for j in range(len(veget_max)):
                    ba_pft[j, i_pft] = 0.0
        # -- Check values of X_scale coefficient:
        x_scale = np.round(x_scale, 9)
        x_ocn   = np.round(x_ocn  , 9)
        for j in range(len(x_scale)):
            if x_scale[j] != x_ocn[j]:
                print(f'Coefficients are different at {j} step:',
                      f'Python X values = {x_scale[j]}'         ,
                      f'OCN X values = {x_ocn[j]}'              )
                sys.exit()
        print('X_scale coefficients were checked. Everything is good. There are no',
              'differences in X_scale coefficient between PYTHON and OCN values \n')
        # -- Check values of fire_fraction:
        # a. Burned fraction calculated in python:
        ffire_pyt = np.round(ba_pft.sum(axis = 1), 6)
        # b. Burned fraction calculated in OCN:
        ffire_ocn = np.round(d_tbaf, 6)
        # Quality control:
        for j in range(len(ffire_pyt)):
            if ffire_pyt[j] != ffire_ocn[j]:
                print(f'Fire fractions are different at {j} step:'   ,
                      f'Python fire_fraction = {ffire_pyt[j]}'       ,
                      f'OCN fire_fraction = {ffire_ocn[j]}'          )
                sys.exit()
        print(
            'Burned fractions were checked. Everything is good. There are no ',
            'differences between fire fraction values in data based on PYTHON and ',
            'OCN algorithms \n'
        )

        # -- Check values of total fire_fraction values:
        print('Check total values:')
        print(
            'Original total values of burned fraction for CLUMP: ',
            fire_frac.sum()
        )
        print(
            'Updated total values of burned fraction for CLUMP: ',
            ba_pft.sum(axis = 1).sum()
        )

# =============================    End of program   ====================
