# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY


## THIS IS THE FILE TO RUN AT FIRST FOR TUTORIAL IN PARTICULAR

import filediag as fd
import bayes_correction_begin_end as be
import bmeta_begin_end as bme
from tkinter import messagebox
import os
import atexit
import bmeta_diag as bd

# routine for the whole UI (bmeta)
def bmeta_ui():
	# root: for the dir and file selection
	
	root = fd.create_root()

	# 1. let the user know that it is time to select the working directory
	messagebox.showinfo("Select working directory", "Please select the working directory. \r\nAll images files and task-related files will be copied.")
	# 2. get working directory (-> workingdir)
	workingdir = fd.set_working_directory(root)
	# 3. let the use know that it is time to select img+hdr or nii files to be analyzed.
	messagebox.showinfo("Select images files to be analyzed", "Please select image files (.hdr or .nii). \r\nAll images files and task-related files will be copied.")
	# 4. get image file list
	filenames = fd.get_image_filenames(root)
	# 5. time to specify which contrast will be analyzed
	messagebox.showinfo("Enter image information","Enter image file information (N size, type of statistics).")
	# 6. create file list in dataframe
	df = bd.create_return_lines(root,filenames)
	# 7. save df in csv
	bd.save_df(workingdir,df)
	# 8. destroy original root
	fd.destroy_root(root)
	# 9. create new root for cpu number input
	root_cpu = fd.create_root()
	# 10. let the user know that it is time to specify the number of cpus to be used
	messagebox.showinfo("Enter CPU number", "Please enter how many CPUs will be used.")
	# 11. get the CPU number
	cpu_num = fd.enter_cpu_num(root_cpu)
	# 12. destroy root_cpu
	fd.destroy_root(root_cpu)
	# 13. create new root for contrast selection
	root_contrast = fd.create_root()
	# 14. time to specify which contrast will be analyzed
	messagebox.showinfo("Select contrast", "Please specify which contrast will be analyzed.\r\ncontrast > 0 or < 0")
	# 15. select contrast
	minus = fd.select_contrast(root_contrast)
	# 16. destroy the root contrast
	fd.destroy_root(root_contrast)
	# 17. time to create run_this.py
	bme.bmeta_run_this(workingdir,cpu_num,minus)
	# 18. copy all files
	bd.copy_all_files_meta(workingdir,df)
	# 19. ask run now after creating a new root
	root_local = fd.create_root()
	# 20. ask whether run_py.py shall be ran on local
	local = fd.select_local(root_local)
	# 21. destroy root_local
	fd.destroy_root(root_local)
	# 22. if local = 1, then run run_this.py
	at_the_end(workingdir,local)

	return 1

# what shall do next?
# if local = 1, then run run_this.py
def at_the_end(workingdir,local):
	if local == 1:
		# end and run
		# move to workingdir
		os.chdir(workingdir)
		atexit.register(lambda: exec(open("run_this.py").read()))
	return 1

# if nothing specified and only bmeta_ui.py is desginated to be excecuted, then run the function
bmeta_ui()