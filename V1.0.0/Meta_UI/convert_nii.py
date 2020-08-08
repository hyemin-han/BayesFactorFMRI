# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


import os
import pandas as pd

# import required nifti processing functions
from nilearn.datasets import load_mni152_template
from nilearn.image import resample_to_img
from nilearn.image import load_img

def convert_nii( lists):
	# create a 91x109x91 MNI template
	template = load_mni152_template()

	# get file list
	list = pd.read_csv(lists)
	filecount = len(list.Filename)
	filenames = [None] * filecount

	# extract file names
	for i in range(0,filecount):
		filenames[i] = os.path.splitext(list.Filename[i])[0]


	# make a folder for outputs
	try:
   		os.mkdir('transformed')
	except OSError as exc:
   	 	pass

#	os.mkdir('transformed')

	# transform (Affine) all current nii files into MNI 152
	for x in range (0,filecount):
		resampled_localizer_tmap = resample_to_img(list.Filename[x], template)
		resampled_localizer_tmap.to_filename('./transformed/%s' % (list.Filename[x]))