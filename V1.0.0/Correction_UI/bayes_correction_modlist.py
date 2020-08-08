# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


import os
import pandas as pd

def bayes_correction_modlist(list):
	# modify the list
	# then create list_mod.csv

	lists = pd.read_csv(list)

	# new file name should be list_mod
	filename = os.path.splitext(list)[0]
	#filename = os.path.split(filename)[1]
	newfilename = filename+"_mod.csv"


	# then get the path of list
	if (os.path.split((list))[0] != ''):
		path = os.path.split(os.path.abspath(list))[0]+"/"
	else:
		path = os.path.split((list))[0]


	# modify pandas dataframe
	lists["Filename"] = path+lists["Filename"]

	# save list_mod.csv
	# in the current directory
	lists.to_csv(newfilename, index=False)

	# return new filename
	return (newfilename)