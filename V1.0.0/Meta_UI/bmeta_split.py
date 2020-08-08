# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


import nibabel as nib
import numpy as np
import math
import pandas as pd

def bmeta_split(newfilename, processes):

	# create list of tasks
	tasks = np.zeros((processes,2),dtype =int)

	# load files
	newfilenames = pd.read_csv(newfilename)
	# get file length
	list_length = len(newfilenames)

	# load mask img
	img = nib.load(newfilenames.Filename[0])
	# get X size
	X = img.shape[0]
	Y = img.shape[1]
	Z = img.shape[2]
	image_data = img.get_fdata()

	imgs = [None] * list_length

	# get img data
	for i in range(list_length):
		img1 = nib.load(newfilenames.Filename[i])
		imgs[i] = img1.get_fdata()

	# loop to create a mask image
	for i in range(X):
		for j in range(Y):
			for k in range(Z):
				# detect non nan and non zero values
				flag = 0
				for l in range(list_length):
					if ((imgs[l][i,j,k] == 0) or (math.isnan(imgs[l][i,j,k]))):
						flag = 1
				# nan
				if flag == 1:
					image_data[i,j,k] = 0
				else:
					image_data[i,j,k] = 1

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

			# only for test
			#print(str(current),str(tasks[current][0]),str(tasks[current][1]),str(currentsum))

			current = current + 1
			start_point = i + 1



	# if the end point of the last process < X (due to some zeros in last Xs), correct it.
	if tasks[processes-1,1] < X:
		tasks[processes-1,1] = X

	return tasks