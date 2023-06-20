#!/bin/bash 

#-------------------------------------------------------------------------------
# Download GFED data from 2002 - 2020 years
#
# Data were calculated based on: https://gmd.copernicus.org/articles/15/8411/2022/
#
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

# =========================== Module settings =======================
module load proxy

# ===========================  User settings ========================
# -- Available GFED data by years:
years=("2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009" "2010" "2011" \
       "2012" "2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020"        )
# -- Prefix for GFED fire emission data:
hindex=("h06" "h07" "h08" "h09" "h10" "h11" "h12" "h13" "h14" "h15" "h16"    \
        "h17" "h18" "h19" "h20" "h21" "h22" "h24" "h25" "h26" "h27" "h28"    \
        "h29" "h30" "h31" "h32" "h33" "h34" "h35"                            )
# -- Prefix for GFED burned area data:
vindex=("v01" "v02" "v03" "v04" "v05" "v07" "v08" "v09" "v10" "v11" "v12"    \
        "v13" "v14"                                                          )
# -- Counts for lists:
ycount=18 # years
hcount=28 # hindex
vcount=12 # vindex
# -- URL with GFED data:
url="https://zenodo.org/record/7229675/files"
# -- Output paths (path was changed because of security reasons):
bOUT="../people/evchur/GFED_2002-2020"
# ============================= Main part ===========================

# -- Clean previous results and create a new log:
log_file=${bOUT}/"Download_GFED.log"

if [ -f "$log_file" ]; then
    echo 'Cleaning previous results'
    rm ${bOUT}/*
fi
touch ${log_file}

# 2. Downloading burned area GFED data:
for (( i=0; i<=ycount ; i++ ));
do
    # Select relevant input file
    file="Model500m_2002-2020yr_025d_"${years[${i}]}".nc"                       # File name
    echo 'Downloading file :' ${file}
    dataIN=${url}/${file}                                                       # Input path (URL)
    dataOUT=${bOUT}/${file}                                                     # Output path
    python3 ./get_GFED.py ${dataIN} ${dataOUT} ${log_file} &                    # Run downloading script
done
sleep 60
echo 'Burned area data were downloaded'
echo ''

# 3. Other GFED parameters
for (( h=0; h<=hcount ; h++ ));
do
    for (( v=0; v<=vcount ; v++ ));
    do
        file="Model500m_2002-2020yr_"${hindex[${h}]}${vindex[${v}]}".nc"
        echo 'Downloading file :' ${file}
        dataIN=${url}/${file}
        dataOUT=${bOUT}/${file}
        python3 ./get_GFED.py ${dataIN} ${dataOUT} ${log_file} &                # Run downloading script
    done
    sleep 60
done
echo 'All GFED data were downloaded'
echo ''
