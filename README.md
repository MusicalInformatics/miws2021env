# Environment for Musical Informatics KV WS 2021

## Setting up a conda environment

1. Go to anaconda.com and download the miniconda (or anaconda, if you prefer) in version compatible with the system your running. You can choose any python version you like, for this course we use 3.7. 
2. Install this software which gives you at least two things: the command-line python package manager ```conda``` (similar to the python package manager ```pip```) and the conda environment management system. Conda environments allow you to create virtual python environments with their own python interpreter and installed packages.
3. In this repository you find a file called ```environment.yml``` which contains a list of dependencies that we use regularly.
4. Create a conda environment with __your_environment_name__ from this file by executing
```
conda env -n your_environment_name -f path/to/environmnent.yml
```
in the terminal of your choice. Conda supports many shells, though some (PowerShell, ...) might require extra steps after installation.
5. You can deactivate the currently active environment by executing
```
conda deactivate
```
6. You can activate your environment by executing
```
conda activate your_environment_name
```
7. In many terminals you see the name of the currently active environment in parnetheses in the beginning of the line. Removing or installing anything via pip or conda will only affect this environment while it is activated. Check your currently installed packages via ```pip freeze``` or ```conda list```. Check the python version using ```python -V```

## Getting started with the first notebook

Make sure to change current directory to this repository on your machine (```cd path/to/repo```) , type ```jupyter notebook``` in your terminal (with activated conda environment) and hit Enter. This will start a jupyter server serving at a link displayed in the terminal. If a browser didn't automatically open, follow the link. In the browser windows you see a an overview of the current directory. Click on intro_to_partitura.ipynb to open the starting notebook...

