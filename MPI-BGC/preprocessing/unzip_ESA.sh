#!/bin/bash

#-------------------------------------------------------------------------------
# Task: Unzip raw ESA-CCI MODIS v5.0 data
#
# Current code owner:
#
#  Max Planck Institute for Biogeochemistry
#
# Authors:
#
#   MPI-BGC, 2022
#   Evgenii Churiulin, Ana Bastos
#   phone:  +49 170-261-51-04
#   email:  evchur@bgc-jena.mpg.de
#
#-------------------------------------------------------------------------------

# =============================== User settings ========================
# ESA-CCI MODIS v5.0 raw data in ZIP format:
years=("2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" \
       "2011" "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020" )
ycount=19

# Main path (This path was changed because of security reasons):
DIR=../scratch/evchur/ESA_DATA/FIRE
# Input fire data:
fDIR_ZIP="${DIR}"/FIRE_ZIP

param="burned_area_in_vegetation_class"
name_out="ESACCI-L4_FIRE-BA-MODIS-fv5.1"

# ============================= Main part ==============================
# Unzip initial data
for (( i=0; i<=ycount ; i++ ));
do
    data_zip="${fDIR_ZIP}"/"${years[${i}]}"."zip"
    unzip "${data_zip}" -d "${DIR}"
    echo "Done: ESA-CCI data were unpacked"
done

# Data processing
#--------------------
for (( i=0; i<=ycount ; i++ ));
do
    data_in="${DIR}"/"${years[${i}]}"
    data_out="${DIR}"/"${name_out}"_"${years[${i}]}".nc
    data_pft="${DIR}"/"${name_out}"_PFT_"${years[${i}]}".nc
    # Create files for 1 year (add 12 month) - all variables
    cdo mergetime  "${data_in}"/*.nc "${data_out}"
    # Move data to a special folder
    mv "${data_out}" "${DIR}"/DATA/
    # Delete folders with monthly data
    rm -R "${data_in}"
    echo "Done: ESA-CCI data were prepared for python script"
done
