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