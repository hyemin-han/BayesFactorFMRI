import filediag as fd
import bayes_correction_begin_end as be
from tkinter import messagebox
import os
import atexit

# routine for the whole UI (bayes_correction)
def bayes_correction_ui():
	# create two Tks
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
	# 5. create list_original.csv based on filenames
	fd.create_list_csv(workingdir, filenames)
	# 6. let the user know that it is time to get mask file
	messagebox.showinfo("Select mask image file", "Please select the mask image file (.hdr or .nii). \r\nmask.nii will be copied.")
	# 7. get the mask filename
	maskfilename = fd.get_mask_filename(root)
	# 8. let the user know that it is time to specify the number of cpus to be used
	messagebox.showinfo("Enter CPU number", "Please enter how many CPUs will be used.")
	# 9. get the CPU number
	cpu_num = fd.enter_cpu_num(root)
	# 10. time to specify which contrast will be analyzed
	messagebox.showinfo("Select contrast", "Please specify which contrast will be analyzed.\r\ncontrast > 0 or < 0")
	# 11. destroy the original root
	fd.destroy_root(root)
	# 12. for contrast window, an independent root should be created
	root_contrast = fd.create_root()
	# 13. select contrast
	minus = fd.select_contrast(root_contrast)
	# 14. destroy the root contrast
	fd.destroy_root(root_contrast)
	# 15. time to create run_this.py
	be.bayes_correction_run_this(workingdir,cpu_num,minus)
	# 16. copy all required files to the designated working directory
	fd.copy_all_files(workingdir,maskfilename)
	# 17. create another root to ask local run
	root_local = fd.create_root()
	# 18. ask whether run_py.py shall be ran on local
	local = fd.select_local(root_local)
	# 19. destroy root_local
	fd.destroy_root(root_local)
	# 20. if local = 1, then run run_this.py
	at_the_end(workingdir,local)

	# Done!
	# Run at local?
	# If not, then let the user know that s/he should upload the working dir and run run_this.py


	return 1

# what shall do next?
# if local = 1, then run run_this.py
def at_the_end(workingdir,local):
	if local == 1:
		# end and run
		# move to workingdir
		os.chdir(workingdir)
		atexit.register(lambda: exec(open('run_this.py').read()))
	return 1

# if a user directly executes this file, then call the function directly
bayes_correction_ui()