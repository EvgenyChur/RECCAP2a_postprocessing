#!/bin/bash

#-------------------------------------------------------------------------------
# Get annual values for LTDR LAI dataset
#
# Current code owner:
#
#  Max Planck Institute for Biogeochemistry
#
# Authors:
#   MPI-BGC, 2022
#   Evgenii Churiulin, Ana Bastos
#   phone:  +49 170-261-51-04
#   email:  evchur@bgc-jena.mpg.de
#-------------------------------------------------------------------------------

# =============================== User settings ==========================
# -- Available years for LTDR dataset:
years=("1981" "1982" "1983" "1984" "1985" "1986" "1987" "1988" "1989" "1990" \
       "1991" "1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" \
       "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" \
       "2011" "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020" )
ycount=39
# -- Research parameter: LAI
param="LAI"
# -- Grid resolution:
lonlat="7200.3600"
# -- Paths:
DIR=..
DIR_IN="${DIR}"/data/DataStructureMDI/DATA/grid/Global/0d050_daily/LTDR/v5/Data/LAI
DIR_OUT="${DIR}"/scratch/evchur/LAI/LAI_0d05_annual

#============================= Main part =======================================
for (( i=0; i<=ycount ; i++ ));
do
    fin="${DIR_IN}"/"${param}"."${lonlat}"."${years[${i}]}"."nc"
    fout="${DIR_OUT}"/"${param}"."${lonlat}"."${years[${i}]}"_"annual"."nc"
    cdo -s -yearmean "${fin}" "${fout}" &
done
