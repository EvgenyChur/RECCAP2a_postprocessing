# -*- coding: utf-8 -*-
"""
Task: Test of the different coefficient values from the OCN model. 
      Equations are presented in pjFire. Values are different in comparison with
      original manuscript.

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-06-30 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-27 Evgenii Churiulin, MPI-BGC
           Updated script structure 
    1.3    2022-11-11 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project
    1.4    2023-02-13 Evgenii Churiulin, MPI-BGC
           Changed output variable (pout)
    1.4    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ================
# -- Standard:
import os
import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.path_settings import output_path
from libraries.lib4sys_support import makefolder
from libraries.lib4visualization import simple_line_plot_settings
# =============================   Personal functions   =================

# =============================   User settings   ======================
# -- Define output paths and create folder for results
pout = makefolder(output_path().get('lpjFire_coef'))
print(f'Your data will be saved at {pout}')

# -- Plot settings for linear plot:
user_line_settings = {
    'labels' : ['OCN', 'ART'],
    'colors' : ['b', 'r'],
    'styles' : ['-', '-.'],
    'title'  : 'Test different equations',
    'xlabel' : 'Annual sum of days with fire conditions',
    'ylabel' : 'Annual fire fraction values',
    'xlims'  : [  0.0, 366.0 , 50.0],
    'ylims'  : [  0.0,   1.01,  0.1],
    'output' : pout + 'lpj_fire_coef.png',
}

# =============================    Main program   ======================
if __name__ == '__main__':
       # -- Calculating values based on different equations:
       s   = np.arange(1, 366, 1) / 365
       xm1 = s - 1
       ffrac_orig = [] # calculations with the coeffients from the article
       ffrac_ocn  = [] # calculations with the coeffients from OCN
       for i in range(len(s)):
           orig_coef = ( 0.45 * xm1[i]**3  + 2.83 * xm1[i]**2 + 2.96 * xm1[i] + 1.09)
           ocn_coef  = (-0.13 * xm1[i]**3  + 0.6  * xm1[i]**2 + 0.8  * xm1[i] + 0.45)
           ffrac_orig.append(pd.Series(s[i] * math.exp(xm1[i] / orig_coef)))
           ffrac_ocn.append( pd.Series(s[i] * math.exp(xm1[i] / ocn_coef )))

       # -- Create datasets:
       df_orig = pd.concat(ffrac_orig, axis = 0).reset_index(drop = True)
       df_ocn  = pd.concat(ffrac_ocn , axis = 0).reset_index(drop = True)
       # -- Create plot:
       fig = plt.figure(figsize = (12,7))
       ax  = fig.add_subplot(111)
       ax.plot(df_ocn.index , df_ocn , label = 'OCN')
       ax.plot(df_orig.index, df_orig, label = 'ART')
       # Apply user settings for linear plot:
       simple_line_plot_settings(ax, user_line_settings)
# =============================    End of program   ====================
