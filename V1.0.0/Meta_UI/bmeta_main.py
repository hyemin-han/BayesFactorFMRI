import rpy2.robjects as robjects
from subprocess import Popen 
import numpy  
from datetime import datetime
import math
import os
import nibabel as nib
import bmeta_split as bcs
import bmeta_modlist as bcm
import convert_nii as cv
import pandas as pd

#import shutil

def bmeta_main( lists, cpus, minus = 0):
	# minus is added at this version
	# to deal with then negative contrast is interested
	# default: contrast > 0

	# declare how many CPUs will be assigned
	processes = cpus

	# if cpus > max cpu in this computer,
	max_cpu = os.cpu_count()

	if processes > max_cpu:
		processes = max_cpu
	
	# first, transform all images
	cv.convert_nii(lists)
	# then modify the list file to take into account relative path
	newfilename = bcm.bmeta_modlist(lists)

	# get X size
	newfilenames = pd.read_csv(newfilename)
	mask = newfilenames.Filename[0]
	img = nib.load(newfilenames.Filename[0])
	X = img.shape[0]

	# create processes
	process = [None] * processes

	flag = [0] * processes

	# get process list
	task = bcs.bmeta_split(newfilename, processes)


	# timestamp: start
	tstart = datetime.now()

	for i in range(processes):
		# start work
		current = task[i,0]
		endpoint = task[i,1]
		#if minus == 0:
			# contrast > 0
		process[i] = Popen(['Rscript','--vanilla','fmri_bmeta_random1.R',str(i),str(current),str(endpoint),newfilename])
		#else:
			# contrast < 0. run minus.
		#	process[i] = Popen(['Rscript','--vanilla','fmri_bmeta_random1_minus.R',str(i),str(current),str(endpoint),newfilename])
		# print current process info (current to endpoint)
		print("Process ID: ", i," Start: ", current, " End:",endpoint)


	while 1:
		# for loop to monitor all processes
		for x in range(processes):
			# the current x process completed?
			if process[x].poll() is not None:
				if flag[x] == 0:
					print("Process ",str(x), "Done!! / total:", str(processes))
				flag[x] = 1
		# all processes completed? -> product should not be 0
		if numpy.prod(flag) > 0:
			# all done
			print('all done!')
			break	

	# successfully ended all the things
	# then reuturn 1

	# endpoint
	tend = datetime.now()
	elapse = tend - tstart
	print (elapse)

	# move output folder to the folder containing list
	#shutil.copy("./output", os.path.split(os.path.abspath(newfilename))[0]+"/output")

	# integrate all the results
	# according to minus
	if minus == 0:
		integrated_result = 0
		r1=robjects.r
		r1.source("integrate_result.R")
		integrated_result = r1.integrate_result(filename = mask)
	else:
		# minus
		integrated_result = 0
		r1=robjects.r
		r1.source("integrate_result_minus.R")
		integrated_result = r1.integrate_result(filename = mask)
	return (integrated_result)
