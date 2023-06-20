# -*- coding: utf-8 -*-

"""
Module has functions for work with file system:
    a. dep_clean --> clean previous results in output folder;
    b. makefolder --> create new output folder;

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-11-11 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2023-05-05 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""

# =============================     Import modules     =====================
import os
import sys
# =============================   Personal functions   =====================
# 1.1 Function --> dep_clean.
def dep_clean(
        path:str,                # Path to the folder with results
    ):
    # -- Start cleaning previous results
    for file in os.listdir(path):
        os.remove(path + file)

# 1.2 Function --> makefolder.
def makefolder(
        # Input variables:
        path:str,                # Input path for output folder
        # OUTPUT variables:
    ) -> str:                    # New path for output data

    # -- Create folder for output data
    try:
        # There is no folder in our output place. Create a new one
        os.makedirs(path)
    except FileExistsError:
        # Folder already exist in our output place.
        pass
    return path + '/'
