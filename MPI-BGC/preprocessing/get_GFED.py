# -*- coding: utf-8 -*-
"""
Description: Download GFED data from 2002 - 2020 years

Data were calculated based on: https://gmd.copernicus.org/articles/15/8411/2022/

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    08.02.23 Evgenii Churiulin, MPI-BGC
           Initial release
"""
# =============================     Import modules     ========================
# 1.1: Standard modules
import sys
from urllib import request
from urllib.error import HTTPError

# =============================   Personal functions   ========================

# ================   User settings (have to be adapted)  ======================
remote_url = sys.argv[1]  
local_file = sys.argv[2]  
log_file   = sys.argv[3]

# =============================    Main program   =============================
logf = open(log_file, "a")
try:
    logf.write("GFED data were downloaded {0} \n".format(str(remote_url)))
    request.urlretrieve(remote_url, local_file)
except HTTPError as error:
    logf.write("Failed to download {0}: {1}\n".format(str(remote_url), str(error)))
# =============================    End of program   ===========================
