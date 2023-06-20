# -*- coding: utf-8 -*-

"""
Task: Create basemap map with random stations location

This version is an initial version of the algorithm which was implemented into 
one_point module. Nevertheless, we can you it for the similar tasks or use it
as an example for further updates.

Autors of project: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-06-25 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2022-10-27 Evgenii Churiulin, MPI-BGC
           Updated script structure 
    1.3    2022-11-16 Evgenii Churiulin, MPI-BGC
           Adapted  for the new format of input functions,
           changed the format of path to the personal modules
    1.4    2023-06-01 Evgenii Churiulin, MPI-BGC
           Code refactoring
"""
# =============================     Import modules     =================
# -- Standard modules:
import os 
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# 1.2 Personal modules
sys.path.append(os.path.join(os.getcwd(), '..')) 
from settings.user_settings import stations
from libraries.lib4sys_support import makefolder
from settings.path_settings import output_path
# =============================   Personal functions   =================

# vis_stations --> Create map with random points (stations)
def vis_stations(
        # Input variables:
        data_OUT:str,            # Output path
        plt_title:str,           # Plot title
        # Output variables:
    ):                           # Create figure in output folder
    # -- Get data for visualization:
    lats = []
    lons = []
    stat = []
    for i in stations:
        lats.append(stations.get(i)[0])
        lons.append(stations.get(i)[1])
        stat.append(stations.get(i)[2])
    # -- Create plot:
    fig = plt.figure(figsize = (12,7))
    ax  = fig.add_subplot(111)
    # -- Create basemap object:
    m = Basemap(projection = 'robin', resolution  = 'l', lon_0 = 0.0, ax = ax)
    x, y = m(lons, lats)
    m.scatter(x, y, marker = 's', s = 25, color = 'm')
    # -- Draw parallels and meridians:
    m.drawparallels(
        np.arange( -90.0,  90.0, 30.0), labels   = [0,1,0,0],
                                        fontsize = 10, 
                                        dashes   = [0.3, 2])
    m.drawmeridians(
        np.arange(-180.0, 180.0, 60.0), labels   = [0,0,0,1],
                                        fontsize = 10,
                                        dashes   = [0.3, 2]) 
    # -- Add relief, coastlines and countries:
    m.shadedrelief(scale = 0.2)
    m.drawcoastlines(linewidth = 0.1)
    m.drawcountries(linewidth  = 0.2, color = 'red', linestyle =  '--' )
    # -- Add labels for stations:
    for label, xpt, ypt in zip(stat, x, y):
        plt.text(xpt-750000, ypt+450000, label, fontsize = 10)
    # -- Add plot title:
    plt.title(f'{plt_title}')
    # -- Save figure and clean memory:
    plt.savefig(data_OUT, format = 'png', dpi = 300)
    plt.close(fig)
    plt.gcf().clear()

# =============================   User settings   ================
# This script uses parameters from other modules. In particularly, you have
# check:
#   1. **/settings/user_settings.py** variable station -> if you want to add
#      or change information about stations, you should change this variable.
#   2. **/settings/path_settings.py** has information about output data path
#      if you want to use another path, change it in modules `/settings/mlocal.py` or
#      `/settings/mcluster.py` function **output_folders**
output_folder = '2dmap4sites'
plot_name = 'STATIONS.png'
plot_title = 'Geolocation of the random points (robinson projection)'

# =============================    Main program   ================
if __name__ == '__main__':
    # -- Define output paths and create folder for results:
    data_OUT  = makefolder(output_path().get(output_folder))
    print(f'Your data will be saved at {data_OUT}')

    vis_stations(data_OUT + plot_name, plot_title)
# =============================    End of program   ==============
