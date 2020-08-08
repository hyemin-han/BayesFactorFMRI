# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


# dealing with the beginning to the end of bmeta UI

import os
import bayes_correction_begin_end as bcbe

# create run this
def bmeta_run_this(workingdir,cpu_num,minus = 0):
	# the format will be
	# from bmeta_main import bmeta_main

	# create text contents
	line1 = "from bmeta_main import bmeta_main\r\n"
	line2 = "bmeta_main(\"list.csv\","+str(cpu_num)+","+str(minus)+")\r\n"

	# write into run_this.py
	outF = open(workingdir+"/run_this.py", "w")
	outF.write(line1)
	outF.write(line2)

	return 1

# run the current runthis after the end of bmeta UI
def run_now(workingdir):
	# call the one in bcbe for efficiency
	bcbe.run_now(workingdir)
	return 1