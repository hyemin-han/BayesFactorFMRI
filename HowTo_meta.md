# GUI directions for Bayesian meta analysis (Tutorial) 

 0. Download all files and sub-folders in "https://github.com/hyemin-han/BayesFMRI/tree/master/V1.0 (codes)" and "https://github.com/hyemin-han/BayesFMRI/tree/master/Meta (tutorial data files)"
 
 1. "python bayes_select_ui.py" in the directory where BayesFMRI codes are downloaded to start the GUI.
 
 2. Select "Bayesian meta-analysis"
 <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/1_task_selection_meta.png" width=50% height=50%>
 
 3. Select a working directory. All files needed for analysis will be copied to hear, so if needed, create an empty new directory and select it.
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/2_working_dir_meta.png" width=50% height=50%>
  
 4. Select statistical image files to be analyzed. For this tutorial, select six nii files. These nii files are available in the directory containing downloaded tutorial data files. For real meta-analysis, these images should be either <i>t</i>-statistics or <i>z</i>-statistics maps created in prior studies to be meta-analyzed.
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/3_img_files_meta.png" width=50% height=50%>
  
 5. Enter study information (for each statistics map). The sample size (<i>N</i>) and type of statistics (<i>t</i> or <i>z</i>) should be speficied for each individual study. For this tutorial, enter the information following the screenshot.
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/4_info_meta.png" width=50% height=50%>
  
 6. Enter how many processors shall be used for analysis. For example, if "4" is entered, Bayesian second-level analysis will be performed with four processors.
   <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/5_cpus_meta.png" width=50% height=50%>
 
 7. Specify which constrast shall be analyzed. For instance, "Contrast > 0" means that BayesFMRI shall test whether the effect size value in each voxel is greater than zero. On the other hand, if "Contrast < 0" is selected, whether the effect size value is smaller than zero is tested. For this tutorial, select "Contrast > 0."
  <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/6_contrast_meta.png" width=50% height=50%>
 
 8. Decide how "run_this.py" is executed. If "End now" is selected, BayesFMRI ends and then users should run "run_this.py" manually. It allows them to upload files to a cluster so that analysis is performed with a high-performance computing system. If "Run on local" is selected, "run_this.py" is executed automatically on local. If users have sufficient number of processors on local, "Run on local" can be selected. If not, "End now" is recommended.
    <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/7_how_to_run_meta.png" width=50% height=50%>
 
 9. One the GUI is closed (and "End now" is selected), all files that are required to perform analysis, i.e., required Python and R codes, config files, statistics image files to be meta-analyzed, run_this.py, are copied to the working directory designated in 3. If users intend to perform analysis on a cluster, upload all files to the cluster. If "End now" is selected, run "python run_this.py," in the working directory to start analysis.
    <img src="https://github.com/hyemin-han/BayesFMRI/blob/master/Images/meta_shots/8_folder_meta.png" width=50% height=50%>
 
 10. Once analysis is completed, in the case of Bayesian meta-analysis, three output files are created. “BFs.nii” shows the resultant Bayes Factor value, “Medians.nii” does the median effect size value, and “Means.nii” does the mean effect size value in each voxel. For hypothesis testing (e.g., whether a significant non-zero effect exists in a voxel), users can open “BFs.nii” with a NIfTI viewer, such as xjView with MATLAB, and perform thresholding (e.g., Bayes Factor ≥ 3).
