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