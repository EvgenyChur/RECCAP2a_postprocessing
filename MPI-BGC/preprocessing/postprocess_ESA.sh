#!/bin/bash

#-------------------------------------------------------------------------------
# Postprocessing script for ESA-CCI data. Script tasks are:
#   a. Implementation the land/ocean mask into natural total burned area fraction
#      data based on ESA-CCI MODIS v5.1 and processed based on python script
#      prep_ESA.py;
#   b. Set a special type of calendar simular to other OCN input files;
#   c. Set a special value for missing values;
#
# Autors of project: Evgenii Churiulin, Ana Bastos
#
# Current Code Owner: MPI-BGC, Evgenii Churiulin
# phone:  +49  170 261-5104
# email:  evgenychur@bgc-jena.mpg.de
#
# History:
# Version    Date       Name
# ---------- ---------- ----
#    1.1    2022-10-26 Evgenii Churiulin, MPI-BGC
#           Initial release
#
#-------------------------------------------------------------------------------

#============================= User settings ===================================

# 1. Select available ESA-CCI data:
years=("2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" \
       "2011" "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020" )
ycount=19

name_out="ba_fraction" # ESA-CCI filename

#=============================== Paths =========================================
# These paths were changed because of security reasons:
DIR=../scratch/evchur/ESA_DATA/FIRE/DATA_PFT
DIR_FIRE=../work_1/RECCAP2/RECCAP_ESACCI/OCNForcing/FIRE
#============================= Main part =======================================

# 2. Create land/ocean mask based on gtopo data
lmask="${DIR}"/LAND_MASK/topo_land.nc
cdo -f nc -setrtomiss,-20000,0 -topo "${lmask}"

# Data processing
#--------------------
for (( i=0; i<=ycount ; i++ ));
do
    data_in="${DIR}"/DATA_IN/"${name_out}"_"${years[${i}]}".nc                  # total burned area for each year
    topo_land_grid="${DIR}"/LAND_MASK/"lmask"_"${years[${i}]}".nc               # land/water mask   for each year
    temp_1="${DIR}"/TEMP/"ftemp1"_"${years[${i}]}".nc                           # temporal burned area data + land/water mask
    temp_2="${DIR}"/TEMP/"ftemp2"_"${years[${i}]}".nc                           # temporal burned area data + land/water mask
    data_out="${DIR}"/DATA_OUT/"lfire_frac"_"${years[${i}]}".nc                 # final burned area data with land/water mask

    # 2.1 Remap mask file to the data grid size of data_in.nc file:
    cdo -f nc -remapcon,"${data_in}" "${lmask}" "${topo_land_grid}"
    # 2.2 Apply land/water mask (topo_land_grid.nc) for burned area data.
    #     Change values of ocean burned fraction pixels to NaN
    cdo -f nc ifthen "${topo_land_grid}" "${data_in}" "${temp_1}"
    # 2.3 Change calendar type
    cdo -setcalendar,standard "${temp_1}" "${temp_2}"
    # 2.4 Change missing values
    cdo -setmissval,-9.e33 "${temp_2}" "${data_out}"
    echo "Done: ESA-CCI data were prepared for: ${years[${i}]} year"
done

# 3. Do you want to delete temporal files?
while true; do
read -p "Do you want to delete temporal files? (y/n) " yn
case $yn in
    [yY] ) rm "${DIR}"/TEMP/*.nc
           echo ok, all temporal files were deleted;
        break;;
    [nN] ) echo ok, all temporal files were saved;
        break;;
    * ) echo invalid response;;
esac
done

# 4. Do you want to copy final data to OCNForcing folder?
while true; do
read -p "Do you want to copy output files to OCNForcing folder? (y/n) " yn
case $yn in
    [yY] ) cp "${DIR}"/DATA_OUT/*.nc "${DIR_FIRE}"/
           chmod 750 "${DIR_FIRE}"/*.nc
           echo ok, all data from DATA_OUT folder were copied to RECCAP_ESACCI/OCNForcing/FIRE/OCNForcing;
        break;;
    [nN] ) echo ok, no copy;
        break;;
    * ) echo invalid response;;
esac
done

echo "Program end"
