# BayesFactorFMRI

<b>Please refer to and cite these articles when you use BayesFactorFMRI:</b>
 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. <i>Cognitive Neuroscience, 11</i>(3), 157-169. http://bit.ly/2S6Uka2
 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. <i>Cognitive Neuroscience, 10</i>(2), 66-76. http://bit.ly/2RCbxZY

<b>BayesFactorFMRI provides a GUI to </b>
 1. Bayesian 2nd-level analysis of fMRI data with multiple comparison correction and
 2. Bayesian meta-analysis of fMRI studies.

To test this tool, R (>= 3.5) and Python (>= 3.7.3; Python 3.8 is not recommended due to package-related issues at this point) are required. Plus, these additional packages should be installed:
 R: BayesFactor, metaBMA, oro.nifti
 Python: tkinter (for GUI), shutil, pandas, nibabel, rpy2, subprocess, numpy, nilearn (os, math, atexit, glob)

 To install dependencies:
 1. R packages <p>
 In the R console, execute: <p>
 install.packages('BayesFactor') <p>
 install.packages('metaBMA')<p>
 install.packages('oro.nifti')<p>

 2. Python packages<p>
 To install the following Python packages, execute the following command at the terminal:<p>
 pip (or pip3) install shutil<p>
 pip (or pip3) install pandas<p>
 pip (or pip3) install nibabel<p>
 pip (or pip3) install rpy2<p>
 pip (or pip3) install subprocess<p>
 pip (or pip3) install numpy<p>
 pip (or pip3) install -U --user nilearn (for further details, refer to https://nilearn.github.io/introduction.html#installing-nilearn)<p>

 After installing all required dependencies, follow directions below:

 1. Download contents (codes and etc.) in V1.0.0.
 2. Download tutorial images files in the designated subfolder(s) (i.e. /Correction for (1) and /Meta for (2)).
 3. Run bayes_select_ui.py with Python to start either correction_ui or bmeta_ui. At the terminal, execute: python bayes_select_ui.py
 4. Follow the directions provided with the GUI.

At the last stage, you will decide either to run the analysis locally or on a cluster.
Once you decide to run the analysis locally, then GUI will call Python and R automatically at the end of the process.
If you choose to run the analysis on a cluster, the GUI will end. You have to upload created files (including both codes, image files, etc.) to a cluster and run run_this.py. These files will be created in a working directory that you specify in GUI. In this process, you may need to write additional code(s) to run run_this.py on the cluster (e.g., slurm batch).

<b> In order to see how to perform Bayesian second-level analysis and meta-analysis with tutorial datasets, please refer to one of these:</b>

[GUI directions for Bayesian second-level analysis (Tutorial)](https://github.com/hyemin-han/BayesFactorFMRI/blob/master/HowTo_2nd.md)

[GUI directions for Bayesian meta-analysis (Tutorial)](https://github.com/hyemin-han/BayesFactorFMRI/blob/master/HowTo_meta.md)

<b>Contact and support</b>
Any bugs, errors, questions, or suggestions associated with BayesFactorFMRI can be submitted via the “Issues” tab in the GitHub repository. Furthermore, the author, Hyemin Han, can be contacted via email for support.
