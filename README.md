# BayesFMRI

<b>Please refer to and cite these articles when you use BayesFMRI:</b>
 1. Bayesian multiple comparison correction: Han, H. (in press). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. <i>Cognitive Neuroscience</i>.
 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. <i>Cognitive Neuroscience, 10</i>(2), 66-76.

<b>BayesFMRI provides a GUI to </b>
 1. Bayesian 2nd-level analysis of fMRI data with multiple comparison correction and
 2. Bayesian meta-analysis of fMRI studies.

To test this tool, R (>= 3.5) and Python (>= 3.7.3) are required. Plus, these additional packages should be installed:
 R: BayesFactor, metaBMA, oro.nifti
 Python: tkinter (for GUI), shutil, pandas, nibabel, rpy2, subprocess, numpy (os, math, atexit, glob)

 1. Download contents (codes and etc.) in V1.0.
 2. Download tutorial images files in the designated subfolder(s) (i.e. /Correction for (1) and /Meta for (2)).
 3. Run bayes_select_ui.py with Python to start either correction_ui or bmeta_ui.
 4. Follow the directions provided with the GUI.

At the last stage, you will decide either to run the analysis locally or on a cluster.
Once you decide to run the analysis locally, then GUI will call Python and R automatically at the end of the process.
If you choose to run the analysis on a cluster, the GUI will end. You have to upload created files (including both codes, image files, etc.) to a cluster and run run_this.py. These files will be created in a working directory that you specify in GUI. In this process, you may need to write additional code(s) to run run_this.py on the cluster (e.g., slurm batch).

<b>GUI directions for Bayesian second-level analysis (Tutorial) </b>
 1. "python bayes_select_ui.py" to start the GUI.
 2. Select "Bayesian correction"
 <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/1_task_selection.png" width=50% height=50%>
 3. Select a working directory. All files needed for analysis will be copied to hear, so if needed, create an empty new directory and select it.
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/2_working_dir.png" width=50% height=50%>
  4. Select contrast image files to be analyzed. For this tutorial, select sixteen nii files, 1.nii-16.nii, except mask.nii.
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/3_img_files.png" width=50% height=50%>
  5. Select a mask image file that designates which voxels should be analyzed. This mask file only consists of 1 vs. 0 or NaN. Only voxels specified with 1 are analyzed by BayesFMRI. A mask file can be created by performing first-order fMRI analysis with widely-used tools, e.g., SPM, AFNI, FSL. For this tutorial, select mask.nii.
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/4_mask_file.png" width=50% height=50%>
  6. Enter how many processors shall be used for analysis. For example, if "4" is entered, Bayesian second-level analysis will be performed with four processors.
   <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/5_cpus.png" width=50% height=50%>
  7. Specify which constrast shall be analyzed. For instance, "Contrast > 0" means that BayesFMRI shall test whether the effect size value in each voxel is greater than zero. On the other hand, if "Contrast < 0" is selected, whether the effect size value is smaller than zero is tested. For this tutorial, select "Contrast > 0."
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/6_contrast.png" width=50% height=50%>
  8. Decide how "run_this.py" is executed. If "End now" is selected, BayesFMRI ends and then users should run "run_this.py" manually. It allows them to upload files to a cluster so that analysis is performed with a high-performance computing system. If "Run on local" is selected, "run_this.py" is executed automatically on local. If users have sufficient number of processors on local, "Run on local" can be selected. If not, "End now" is recommended.
    <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/7_how_to_run.png" width=50% height=50%>
    9. One the GUI is closed (and "End now" is selected), all files that are required to perform analysis, i.e., required Python and R codes, config files, contrast image files, mask image file, run_this.py, are copied to the working directory designated in 3. If users intend to perform analysis on a cluster, upload all files to the cluster. If "End now" is selected, run "python run_this.py," in the working directory to start analysis.
    <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/correction_shots/8_folder.png" width=50% height=50%>
    10. Once analysis is completed, in the case of Bayesian second-level analysis, two output files are created. “BFs.nii” reports the resultant Bayes Factor value in each voxel and “Ds.nii” reports the median effect size value in Cohen’s D in each voxel. For hypothesis testing (e.g., whether a significant non-zero effect exists in a voxel), users can open “BFs.nii” with a NIfTI viewer, such as xjView with MATLAB, and perform thresholding (e.g., Bayes Factor ≥ 3).
  
