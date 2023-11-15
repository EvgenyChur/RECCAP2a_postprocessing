#!/bin/bash 

#-------------------------------------------------------------------------------
# Running script for the main postprocessing system.
#
# Important: Before running this script you have adapt 2 additional files with settings:
# 1. \settings\user_settings.py --> settings for datasets, timeperiods, logical parameters and ets.;
# 2. \settings`path_settings.py --> settings for data paths. If you are working
#                                   on MPI-BGC cluster you have to adapt only output paths.
#                                   Input data can be the same;
# 3. If you are working on different cluster you have to prepare your data before
#
# Current code owner: Max Planck Institute for Biogeochemistry
#
# Authors: MPI-BGC, 2022
#          Evgenii Churiulin, Ana Bastos
#          phone:  +49 170-261-51-04
#          email:  evchur@bgc-jena.mpg.de
#-------------------------------------------------------------------------------

# ================   User settings (have to be adapted)  ===================

# -- Research domains:
# There are 5 different research domains which have already been implemented
# into the fire_xarray.py postprocessing system ("Global", "Europe", "Tropics",
# "NH" and "Other"). I didn't tested "NH" and "Other". If want to add new one -
# just change "Other" to your personal domain or just add new.
domain=("Global")

# -- Research parameters:
# At the moment you can use different output parameters of OCN, JULES, ORCHIDEE models
# and compare them with satellite data and in-situ data. The full list of parameters is
var=("burned_area" "cVeg" "npp" "gpp" "lai" "nee" "nbp" "fFire")
#var=("burned_area") #"cVeg" "npp" "gpp" "lai" "nee" "nbp" "fFire")

# -- Counters (start from 0):
dcount=0 # domain count
vcount=7 # var count

# -- Parameters for output folder (define only name of output folder):
year_start=1980 # first year
year_stop=2010  # last year

# -- Output path for the results folder:
pOUT=../scratch/evchur/RESULTS
fout=${pOUT}/RECCAP2_${year_start}_${year_stop}

# ============================= Main part ==================================
# -- Cycle over domains:
for (( i=0; i<=dcount ; i++ ));
do
    # -- Cycle over parameters:
    for (( j=0; j<=vcount ; j++ ));
    do
        # -- Run main python script for data postprocessing:
        python3 ./fire_xarray_RECCAP2A_domains.py ${year_start} ${year_stop} ${domain[${i}]} ${var[${j}]}
    done
done
# -- Create output folder:
if [[ ! -e $pout_ndep ]]; then
    echo "Creating output folders:"
    mkdir ${fout}
fi
# -- Move folders with parameters results to the new one:
for (( j=0; j<=vcount ; j++ ));
do
    mv ${pOUT}/${var[${j}]} ${fout}
done
# =============================    End of program   =======================