# -*- coding: utf-8 -*-
"""
Task: Create timeseries of random years (Data can be used for OCN model)

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-09-15 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-11-16 Evgenii Churiulin, MPI-BGC
           Set enviroments to personal modules, adapted to global MPI-BGC project 
    1.3    2023-02-13 Evgenii Churiulin, MPI-BGC
           Changed output variable (data_OUT)
    1.4    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     ==================
import os
import sys
import numpy as np
import pandas as pd
import random
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings import logical_settings, get_output_path
from libraries import makefolder
# =============================   Personal functions   ==================

# =============================    Main program   =======================
if __name__ == '__main__':
       # =============================   User settings   ================
       # Load basic user logical settings:
       lsets = logical_settings(lcluster = True)

       # -- Get output paths and create folder for results
       data_OUT = makefolder(get_output_path(lsets).get('rand_ts4s0'))
       pout     = data_OUT + 's0_seq_years.txt'
       print(f'Your data will be saved at {pout}')

       first_year = 1950 # first year
       last_year = 1959  # last year
       niter = 10000     # numbers of iterations

       # -- Create timeseries:
       iterations = np.arange(1, niter, 1)
       # -- Add random values in range 1950 - 1959
       s0 = []
       for i in iterations:
           index_line = pd.Series(i)
           years = pd.Series(random.randint(first_year, last_year))
           result = pd.concat([index_line, years], axis = 1)
           s0.append(result)
       df = pd.concat(s0, axis = 0)
       # -- Save file:
       np.savetxt(pout, df.values, fmt='%d')
# =============================    End of program   =====================
