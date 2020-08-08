# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


import nibabel as nib
import numpy as np

def bayes_correction_split(mask, processes):

	# create list of tasks
	tasks = np.zeros((processes,2),dtype =int)

	# load mask img
	img = nib.load(mask)
	# get X size
	X = img.shape[0]
	# get img data
	image_data = img.get_fdata()

	# get total voxel num to be tested
	total_voxel = np.sum(image_data)

	# get average voxel num for each process
	ave_voxel = total_voxel/processes

	current = 0
	currentsum = 0
	start_point = 0

	# loop
	for i in range(X):
		currentsum = currentsum + np.sum(image_data[i])
		if (currentsum >= ave_voxel*(current+1)):
			# time to record and move on to the next processes
			# because the values will be sent to R, should be +1
			tasks[current][0] = start_point+1
			tasks[current][1] = i+1
			current = current + 1
			start_point = i + 1

	# if the end point of the last process < X (due to some zeros in last Xs), correct it.
	if tasks[processes-1,1] < X:
		tasks[processes-1,1] = X

	return tasks