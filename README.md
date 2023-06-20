# ESA-CCI RECCAP2A

## Project description:
In the previous phase of ESA-CCI RECCAP-2, it has been shown that the global datasets used in to produce the Global Carbon Budgets show large discrepancies at the scale of small regions. These discrepancies were explained by (i) poor agreement between atmospheric inversions and dynamic global vegetation models (DGVMs) in the sensitivity to climate variability and long-term trends, (ii) possible errors in the land-cover datasets used in the global runs, (iii) poor representation of disturbances such as fire. In spite of these known issues, DGVMs have the advantage that they allow to attribute changes in net CO2 fluxes and biomass changes to specific processes and to human-driven vs. natural processes. 
DGVMs have limited ability to simulate spatial-temporal patterns of fire emissions and currently do not simulate agricultural fires. Here, we want to evaluate the potential for assimilating satellite-based burned area data in order to deliver improved carbon budgets from country to global scale. For this, we will conduct two sets of simulations, one with prognostic burned area (prognostic BA simulation) and another with prescribed burned area based on ESA Fire-CCI (diagnostic BA simulation). To avoid double counting of fire emissions from deforestation, we run simulations with fixed land-cover map. The resulting spatio-temporal patterns of carbon fluxes and biomass changes will be compared with other datasets in RECCAP2-A.  

More information about RECCAP2 project is available in [the protocol][link1] and an [official web-page][link2] of the project.

![fig](https://github.com/EvgenyChur/RECCAP2a_postprocessing/blob/main/RESULTS/ADDITIONAL_MATERIALS/RESULTS.jpg)

**Figure 1:** Comparison output model results before (S2Diag) and after updating (S2Prog) models, based on: a) burned area fraction, b) fire emissions.

## Content of RECCAP2A project:
Project has 2 main folders:
1. `MPI-BGC` -> has modules for RECCAP2A data processing. All modules were splitted by subfolders depending on their purpose:
    - ***calc*** -> modules with controlling functions for statistical analysis, visualization and one point (station) computations;
    - ***libraries*** -> modules with functions for data processing;
    - ***main*** -> main running scripts;
    - ***notes*** -> useful notes for future developments;
    - ***preprocessing*** -> modules with functions for data preprocessing;
    - ***settings*** -> modules with user settings;
    - ***tests*** -> small scripts with a local task or simplified algorithm which were implemented into main running scripts.

Each subfolder has an additional readme.md file with more detailed information.

2. `RESULTS` -> examples of output figures;

3. `README.md` -> current file;


## Cloning RECCAP2A processing scripts:
In order to use/develop RECCAP2A processing scripts repository should be cloned. To clone from gitlab, you need to provide a valid public key or use HTTPS connection. In the latter case, you have to write your login and password everytime when you want to do something with gitlab server. More information is available on the official gitlab web-page ([how to use SSH keys to communicate with Github][2]):

If you want to continue developing of *RECCAP2A* processing scripts you have to do the next things:
1. Open the web version of *RECCAP2A* project and create `a new issue` with the name of your research or task. Name should gives other users the key aspect of your work;
2. From your new issue, you have to create a new branch with the name **/feature/{direction_of_your_updates}**. You have to use a branch `main` as a source branch;
3. At the moment, your new branch is a full copy of the main branch and you can clone it to your "local" computer:
```
git clone --branch /feature/{direction_of_your_updates} git@github.com:EvgenyChur/RECCAP2a_postprocessing.git reccap2a_scripts
cd reccap2a_scripts
git status
```
4. If you want to add changes into RECCAP2A scripts you have to use these commands:
```
git status
git add *
git commit -m 'your commit name'
git push
```
Now all your changes are visible in web-version and you can check them.
5. If you want to `merge` your updates to the main branch you have to `create a new merge reguest`;
6. Sometimes, you branch can have the older version that the source branch and if you want to update your branch to the last version of source branch you can use:
```
git pull
```
However, your updates will be replaced by the updated version. More information about git command you can find in Google!


***P.S.1: You have to change these name {direction_of_your_updates} and {your commit name} to yours***

***P.S.2: Don't forget that before you start working with RECCAP2A processing scripts on MPI-BGC SLURM cluster or your local computer, you have to plug SLURM modules, install and set your enviroments for miniconda (anaconda), set git parameters (user.name and user.email), set a valid public key for GitLab. More information about you can find in MPI-BGC discourse. The main useful links are presented in section Additional materials***

## Additional materials:
There are a lot of useful information in MPI-BGC discourse platform for communication. For example:
1. **BGC SLURM cluster**:
    - [Introduction to BGC slurm-cluster][9]
    - [BGC slurm-cluster basics][10]
    - [Basic introduction to the BGC slurm-cluster][11]

2. **Python instructions**:
    - [Setting up Python/IPython/Jupyter on the slurm-cluster][6]
    - [Python code publishing recipes and info][7]
    - [How-to embarassingly parallel Python Jobs on BGC Slurm cluster][8]

3. **Git usage tutorials**:
    - [General information about git][3] and more detailed discussion [how to use gitlab on MPI-BGC cluster][4];
    - [Using Github on MPI-BGC cluster][5];

Don't forget to get access to MPI-BGC Discourse.

[link1]: https://git.bgc-jena.mpg.de/abastos/esa-cci-reccap2a/-/blob/Version_19082022/REPORTS/RECCAP2-A_Protocol.docx
[link2]: https://climate.esa.int/en/projects/reccap-2/

[2]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
[3]: https://bgc.discourse.mpg.de/t/git-usage-tutorial/40
[4]: https://bgc.discourse.mpg.de/t/git-usage-tutorial-discussion/3049
[5]: https://bgc.discourse.mpg.de/t/using-github-on-cluster-development-nodes/3711
[6]: https://bgc.discourse.mpg.de/t/setting-up-python-ipython-jupyter-on-the-slurm-cluster/2975
[7]: https://bgc.discourse.mpg.de/t/python-code-publishing-recipes-and-info/2132
[8]: https://bgc.discourse.mpg.de/t/how-to-embarassingly-parallel-python-jobs-on-bgc-slurm-cluster/3691
[9]: https://bgc.discourse.mpg.de/t/introduction-to-bgc-slurm-cluster/3142
[10]: https://bgc.discourse.mpg.de/t/bgc-slurm-cluster-basics/3482
[11]: https://bgc.discourse.mpg.de/t/basic-introduction-to-the-bgc-slurm-cluster/3663

## Errors:
1. You can get this error -> `PuTTY X11 proxy: unable to connect to forwarded X server: Network error: Connection refused`. Don't panic the main problem is that figure cannot be open on MPI-BGC cluter. To fix it, you can install Xming or open the figure later. This problem is common for Windows system;

