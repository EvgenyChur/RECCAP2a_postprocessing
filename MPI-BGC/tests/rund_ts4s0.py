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
# -- Standard:
import os
import sys
import numpy as np
import pandas as pd
import random
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
from settings.path_settings import output_path
from libraries.lib4sys_support import makefolder
# =============================   Personal functions   ==================

# =============================   User settings   =======================
# -- Get output paths and create folder for results
data_OUT = makefolder(output_path().get('rand_ts4s0'))
pout     = data_OUT + 's0_seq_years.txt'
print(f'Your data will be saved at {pout}')

first_year = 1950 # first year
last_year = 1959  # last year
niter = 10000     # numbers of iterations
# =============================    Main program   =======================
if __name__ == '__main__':
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
