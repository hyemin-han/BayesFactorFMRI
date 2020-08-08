# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


# create run_this.py to run bayes_correction
# and merge results into thresholded image files
# input: working directory, number of cpu
# run_this.py will be created in the designated working directory

import os
import rpy2.robjects as robjects

# to create run_this.py
def bayes_correction_run_this(workingdir,cpu_num,minus = 0):
	# the format will be
	# from bayes_correction_main import bayes_correction_main
	# bayes_correction_main('mask.nii','list.csv',cpu_num)
	# mask file should be mask.nii 

	# Additional: minus specified?

	# move to the designated working directory
	# should not move
	#os.chdir(workingdir)

	# create text contents
	line1 = "from bayes_correction_main import bayes_correction_main\r\n"
	line2 = "bayes_correction_main(\"mask.nii\",\"list.csv\","+str(cpu_num)+",0,"+str(minus)+")\r\n"

	# write into run_this.py
	outF = open(workingdir+"/run_this.py", "w")
	outF.write(line1)
	outF.write(line2)
	return 1

# in addition, once all calculations are done, call this function to merge results
def bayes_correction_merge_results(workingdir):
	# move to workingdir
	os.chdir(workingdir)
	# run integrate_result.R
	#os.system("Rscript --vanilla "+workingdir+"/integrate_result.R")
	# call the R function
	r1=robjects.r
	r1.source("integrate_result.R")
	integrated_result = r1.integrate_result("mask.nii")

	return 1

# if the user wants to run run_this.py right now, then allow to do so
def run_now(workingdir):
	os.chdir(workingdir)
	os.system("python run_this.py")
	return 1