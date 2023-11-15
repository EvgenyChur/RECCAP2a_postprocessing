# -*- coding: utf-8 -*-
__all__ = [
    'dep_clean',
    'makefolder',
]
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
    1.3    2023-11-09 Evgenii Churiulin, MPI-BGC
           Added package import
"""

# =============================     Import modules     =====================
import os
import sys
# =============================   Personal functions   =====================
def dep_clean(path:str):
    """Cleaning previous results:"""
    for file in os.listdir(path):
        os.remove(path + file)

# 1.2 Function --> makefolder.
def makefolder(path:str) -> str:
    """Make new output folder:"""
    try:
        # There is no folder in our output place. Create a new one
        os.makedirs(path)
    except FileExistsError:
        # Folder already exist in our output place.
        pass
    return path + '/'
