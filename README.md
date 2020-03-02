# BayesFMRI

BayesFMRI provides a GUI to 
 1. Bayesian 2nd-level analysis of fMRI data with multiple comparison correction and
 2. Bayesian meta-analysis of fMRI studies.

To test this tool, R (>= 3.5) and Python (>= 3.6.5) are required. Plus, these additional packages should be installed:
 R: BayesFactor, metaBMA, oro.nifti
 Python: tkinter (for GUI), shutil, pandas, nibabel, rpy2, subprocess, numpy (os, math, atexit, glob)

 1. Download contents (codes and etc.) in V1.0.
 2. Download tutorial images files in the designated subfolder(s) (i.e. /Correction for (1) and /Meta for (2)).
 3. Run bayes_select_ui.py with Python to start either correction_ui or bmeta_ui.
 4. Follow the directions provided with the GUI.

At the last stage, you will decide either to run the analysis locally or on a cluster.
Once you decide to run the analysis locally, then GUI will call Python and R automatically at the end of the process.
If you choose to run the analysis on a cluster, the GUI will end. You have to upload created files (including both codes, image files, etc.) to a cluster and run run_this.py. These files will be created in a working directory that you specify in GUI. In this process, you may need to write additional code(s) to run run_this.py on the cluster (e.g., slurm batch).
