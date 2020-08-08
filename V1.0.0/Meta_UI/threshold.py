# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


import glob
import os
import math
import numpy as np

# threshold Means.nii or Medians.nii based on a given BF threshold
# it is to find out which voxel showed significant r != 0 supported by evidence

# import required nifti processing function(s)
import nibabel as nib

# load BFs.nii
BFimg = nib.load('BFs.nii')
BFdata = BFimg.get_data()

# get some parameters
# 1. BF threshold (in 2logBF)
# 2. Mean or median?

BF = float(input('1. BF threshold in 2logBF? (Guideline: 2: Positive, 6: Strong, 10: Very strong (Kass & Raftery, 1995)'))
logBF = BF

# transform from 2logBF to BF
BF = math.exp(BF / 2.0)

# use Mean or median?
MM = int(input('1. Use Mean(1) or Median(2)?'))


if MM == 1:
	# Threshold Means.nii
	# load image
	Curimg = nib.load('Means.nii')
	Type = 'Mean'

if MM == 2:
	# load image
	Curimg = nib.load('Medians.nii')
	Type = 'Median'

Curdata = Curimg.get_data()

# Direction
Direction = int (input('1. + thresholding? 2. - thresholding? 3. bi-direction?'))

if Direction == 1:
	Sign = '+'
if Direction == 2:
	Sign = '-'
if Direction == 3:
	Sign = 'all'

# Create result image
Result = np.zeros((91,109,91))

# treshold image. if current voxel BF < threshold, mark it with zero.
for x in xrange(1,91):
	for y in xrange(1,109):
		for z in xrange(1,91):

			# is NaN?
			if (np.isnan(BFdata[x][y][z])):
				# Then, mark the current voxel as NaN
				Result[x][y][z]=np.nan
				continue

			# Smaller than the threshold or not
			if (BFdata[x][y][z] < BF):
				Result[x][y][z] = 0
			else:
				# defending on the Sign
				if Direction == 3:
					# bi-direction
					Result[x][y][z] = Curdata[x][y][z]
				if Direction == 1:
					# only A>B (+)
					if Curdata[x][y][z] >0:
						Result[x][y][z] = Curdata[x][y][z]
					else:
						Result[x][y][z] = 0
				if Direction == 2:
					# only A<B (-)
					if Curdata[x][y][z] <0:
						Result[x][y][z] = Curdata[x][y][z]
					else:
						Result[x][y][z] = 0	

	
# create resultant image
array_img = nib.Nifti1Image(Result, BFimg.affine)
# save thresholded image
filename =('2logBF_%f_%s_%s.nii' %(logBF,Type,Sign))
nib.save(array_img, filename)