# Scripts description:

Scripts from this folder has several purposes:
* solve a small task which are related to data processing or visualization;
* test a simplified version of the algorithm which can be implemented into OCN model or post-processing scripts from `main` folder;
* test OCN algorithms based on equations and check which potential values can be calculated in them;

1. `2dmap4sites.py` - create a global map as a Basemap object with information about random station location. Information about stations comes from `station` dictionary **/settings/user_settings.py**. More complicated option of this script (***vis_stations***) has been implemented into `libraries/lib4visualization.py` and the controlling function is located in `calc/one_point.py`.
![result_1](https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/2D_MAP/STATIONS.png)

2. `ctr_alg4ocn.py` - script for testing mathematical algorithm for calculation of burned area fraction based on ESA-CCI initial data. This algorithm has been implemented into ***OCN*** model, subrotine ***LPJ_fire***. The main idea is input total burned area fraction values of ESA-CCI MODISv5.0 should be the same before and after calculation of OCN model. We can get this result if we use scalling coefficients calculated based on different plant functional types and fire resistance coefficients. This script can you understanding how the new OCN algorithm for burned area works. Script uses the raw output results of OCN model, which were printed in OCN model log and copied as numpy arrays in `tests/ocn_data4ctr_alg.py`.

3. `ocn_data4ctr_alg.py` - the auxiliary module with information from modernized log files of OCNv202302. I used this module as source of raw OCN data for testing new fire algorithm from `ctr_alg4ocn.py` on OCN model grid. Data presented for one OCN CLUMP.

4. `ctr4ocn_out.py` - script for controlling OCN outputs at different steps:
   - Direct output from OCN model - data for one CLUMP;
   - Data after aggregation of data for global map (all CLUMPs together);
   - Data after TRENDY output postprocessing.
After updates, I had a problem that input and output `ESA-CCI MODIS v5.0` data were different. Nevertheless, the `ctr_alg4ocn.py` script gave me correct values. Due to I created this script and found that problem was with aggregation of OCN burned area data for a global map. Because of that, I changed OCN post-processing scripts.

5. `ctr_interpolation.py` - script for controlling burned area fraction before and after interpolation data to OCN grid. Values of burned area fractions calculated based on OCN model with different settings (exp S2.1 and S2.2) presented on different spatial resolution grids. Results of interpolation from 1.0 deg grid to 0.5 deg grid should be the same, because we are working with areas. If results are different - our method of interpolation doesn't work. (In general we have to use upscalling). Actual algorithm for upscalling is presented in the script - `/preprocessing/upscaling_mode.py`.

6. `fast_test.py` - script for comparing burned area fraction of *ESA-CCI MODISv5.0* dataset and *OCN* model by PFT. Script can create linear plots and global maps. Also script has instrument for comparison data presented on different grids (original - `720*1440` and OCN `360*720`) and you can select and use only ESA-CCI natural PFT;

|     Plot_1  |     Plot_2  |    Plot_3   |
|:-----------:|:-----------:|:-----------:|
| ![][fig6_1] | ![][fig6_2] | ![][fig6_3] |

|  ESA-CCI MODIS (nat PFT) |  OCN PFT    |  DIFF (ESA - OCN)  |
|:------------------------:|:-----------:|:------------------:|
|      ![][fig6a]          | ![][fig6b]  |  ![][fig6c]        |

[fig6_1]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/FAST_TEST/BA.png
[fig6_2]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/FAST_TEST/BA_PFT.png
[fig6_3]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/FAST_TEST/BA2BA_PFT.png
[fig6a]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/FAST_TEST/2D_map4MODIS.png
[fig6b]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/FAST_TEST/2D_map4OCN.png
[fig6c]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/FAST_TEST/2D_map4DIFF.png

7. `ffire_test.py`- script for comparing GFED4.1s fFire data presented on different grids (original - `720*1440` and OCN `360*720`);

|  fFire (Annual values) | fFire (grig - `1440*720`) | fFire (grig - `720*360`) |
|:----------------------:|:-------------------------:|:------------------------:|
|      ![][fig1]         |       ![][fig2]           |        ![][fig3]         |

[fig1]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/fFIRE_TEST/annual_fFire.png
[fig2]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/fFIRE_TEST/fFire_720_1440.png
[fig3]: https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/fFIRE_TEST/fFire_360_720.png

8.  `GFED2.py` - script for testing the new generation of GFED2 data. Simple script for reading NetCDF data and analysis of it's attributes, time units and ets.

9. `rand_ts4s0.py` - script for creating random timeseries ***s0_sequence.txt***. The file is required for running OCN model (mixing years for SPINUP);

10. `lpjFire_coef.py` - a simple test of coefficient values used in `lpjFire.f90` module of **OCN** model. OCN values are different from the original paper. Because of that this test was created.
![result_10](https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/LPG_COEF/lpj_fire_coef.png)

11. `OCN_param.py` - a script with the simplified version of the calculation algorithm implemented in `/main/fire_xarray.py`. You can use it only for one research parameter. Can be usefull, if you want to add new datasets for analysis.
![result_11](https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/TESTS/FIGURES/OCN_PARAM/BA_Global.png)

12. `test_jules.py` - script for testing *JULES output model* results. More complicated version of thealgorithm have been implemented into the `main` postprocessing scripts.

## How to set scripts?
1. `ctr_alg4ocn.py` --> check values in section **User settings**. In case of 1 point algorithm you can change values of fire resistance and land cover fraction manually. But if you want to use algortithm with output OCN data you can use my data which I got from **OCNv202302 log files** and copied into `ocn_data4ctr_alg.py` or you can create you new log files and use them. Save changes and run;

2. `OCN_param.py` --> check values in section **User settings** and you have to set time limits for OCN data in `settings/user_settings.py`

3. **Other scripts** --> check values in section **User settings**, save and run;

## How to run scripts?
If you want to run script you have to use next commands:
```
cd your_path\MPI-BGC\tests\
python3 ./script_name.py
```
where: `your_path` is absolute data path, `script_name` is script name. These parameters shpould be adapted by users.


<span style="color:red"><strong><em>Important information:</em></strong></span>
If you want to find place, where the module or function has been applying you can use this command:
```
grep -rn your_string folder
```
where: `your_string` is what you want to find; `folder` is folder where you want to search.