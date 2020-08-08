# BayesFactorFMRI: This is a GUI-aided tool to perform Bayesian meta-analysis of fMRI data and Bayesian second-level analysis of fMRI contrast files (one-sample t-test) with multiprocessing.
# author: Hyemin Han, University of Alabama (hyemin.han@ua.edu)
# BayesFactorFMRI is licensed under MIT License.

# Citations
# In addition to the Journal of Open Research Software paper,
# 1. Bayesian multiple comparison correction: Han, H. (2020). Implementation of Bayesian multiple comparison correction in the second-level analysis of fMRI data: With pilot analyses of simulation and real fMRI datasets based on voxelwise inference. Cognitive Neuroscience, 11(3), 157-169. http://bit.ly/2S6Uka2
# 2. Bayesian meta-analysis: Han, H., & Park, J. (2019). Bayesian meta-analysis of fMRI image data. Cognitive Neuroscience, 10(2), 66-76. http://bit.ly/2RCbxZY

from tkinter import *
from tkinter import filedialog
import shutil
import pandas as pd
import os
import nibabel as nb
import tkinter as tk
from tkinter import messagebox

# create a root Tk for further UIs
# should be called at the initiation of bayes_correction
def create_root():
	# create a root
	root=Tk()
	return root

# destroy a root upon the end of the program
# should be called at the end of bayes_correction
def destroy_root(root):
	# destroy root
	root.destroy()
	return 1

# function to specify multiple image files
def get_image_filenames(root):
	# open a dialog
	filenames = filedialog.askopenfilenames(initialdir=".",title="Select Image Files (nii, hdr)", filetypes=[("Img files","*.hdr *.nii")])
	# return the filelist
	return filenames

# specify a directory to copy all require files
def set_working_directory(root):
	# pop a dialog to select a working directory (all required filed will be copied to)
	directory = filedialog.askdirectory()
	# return the directory info
	return directory

# create list.csv based on filenames
# a working directory should be already set
# also, a list of image files should be received
def create_list_csv(workingdir, filenames):
	# first, create a dataframe based on "filenames"
	# FYI, filename is a list, so should be transformed into a df with pandas (pd)

	# create a df from filenames
	df = pd.DataFrame(filenames,columns=['Filename'])
	# save into working dir
	df.to_csv(workingdir+'/list_original.csv',index=False)

	return 1

# function to specify mask file
def get_mask_filename(root):
	# open a dialog
	mask_filename = filedialog.askopenfilename(initialdir=".",title="Select a Mask Image File (nii, hdr)", filetypes=[("Img files","*.hdr *.nii")])
	# return the filelist
	return mask_filename

# copy all required files
# a working directory should be already set
# required files
# python codes: bayes_correction_main.py, bayes_correction_modlist.py, bayes_correction_split.py
# R codes: Bayes_segment.R, correct_scale.R, integrate_result.R
# list.csv
# image files specified in filenames
# list.csv should be already created and exist in the workingdir

# PLUS, mask file!

def copy_all_files(workingdir,mask_filename):
	# define the list of required source files	
	# first, python codes
	py_list = ['bayes_correction_main.py','bayes_correction_modlist.py','bayes_correction_split.py']
	# get the number of py files
	py_num = len(py_list)
	# then, R files
	R_list = ['Bayes_segment.R','Bayes_segment_minus.R', 'correct_scale.R', 'integrate_result.R']
	# get the number of R files
	R_num = len(R_list)

	# start a for loop for copying py files
	for i in range(py_num):
		# copy files
		shutil.copy2(py_list[i], workingdir)

	# then, a loot for copying R files
	for i in range(R_num):
		# copy files
		shutil.copy2(R_list[i],workingdir)

	# load list_original.csv
	# and then conver to the current folder
	list = pd.read_csv(workingdir+'/list_original.csv')
	files = list.Filename
	files_num = len(files)
	pure_filenames = [None] * files_num

	# copy image files to the working dir
	for i in range(files_num):
		shutil.copy2(files[i],workingdir)

		# if this is a hdr, then img should also be copied
		# if this is a img, then hdr should also be copied
		# split extension
		filename, file_extension = os.path.splitext(files[i])
		if (file_extension =='.hdr'):
			# then, copy img as well
			img_file = filename+'.img'
			shutil.copy2(img_file,workingdir)

		# then convert to list.csv (removing directory designation)
		pure_filenames[i] = os.path.basename(files[i])
	# then save to list.csv
	df = pd.DataFrame(pure_filenames,columns=['Filename'])
	df.to_csv(workingdir+'/list.csv',index=False)

	# finally, copy mask file
	filename, file_extension = os.path.splitext(mask_filename)
	
	# if hdr, then convert to nii
	if (file_extension==".hdr"):
		img = nb.load(mask_filename)
		newfilename = workingdir + '/mask.nii'
		nb.save(img,newfilename)
	else:
	# if not, then just copy
		shutil.copy2(mask_filename,workingdir+'/mask.nii')

	return 1

# remove directory designation from filelist
# then, return the list of files without directory info
# all to "."



# get which contrast will be calculated
# minus = 0 -> + contrast
# minus = 1 -> - contrast
# for this purpose, there should be an independent TK should be created
def select_contrast(root):
	# create a new window
	#nowroot = create_root()
	var = tk.IntVar()
	var1 = tk.IntVar()
	# set the window bigger
	root.minsize(width=200, height=200)

	# get frame of new root
	#frame=Frame(nowroot)
	#frame.pack()
	# default, minus = 0
	minus = 0

	# place two radio buttons
	Radiobutton(root ,text="Contrast > 0",value=0,variable = var1).grid(row = 0,column = 0)
	Radiobutton(root,text="Contrast < 0",value=1,variable = var1).grid(row = 1,column = 0)
	# set default (plus)
	var1.set(0)

	# create button and set it to be ended
	button = tk.Button(root,text="Confirm", command = lambda:var.set(1))
	button.place(relx=.5, rely=.5, anchor="c")
	
	# button clicked
	button.wait_variable(var)
	# close the window
	#destroy_root(nowroot)
	minus = var1.get()

	# clear
	clear_widgets(root)
	return minus

# get CPU number
# if non-number value is entered, print error and ask to enter num once again
def enter_cpu_num(root):
	# default = 1
	cpu_num =1
	# set interface variable
	var = tk.IntVar()
	var1 = tk.IntVar()
	# set the window bigger
	root.minsize(width=200, height=200)
	# set default (plus)
	var1.set(1)

	# create button and set it to be ended
	button = tk.Button(root,text="Confirm", command = lambda:var.set(1))
	button.place(relx=.5, rely=.5, anchor="c")

	# create entry widget
	text1 = tk.Entry(root, validate='key')
	text1.grid()
	text1.focus()
		

	# while loop...
	# wait until we get a correct int value > 0
	while(1):
		# button clicked
		button.wait_variable(var)	

		# get entry
		result = text1.get()
		# check whether the entry is correct
		# is numeric?
		if result.isnumeric():
			value = int(result)
		else:
			value = -1

		if (value > 0):
			# should be greater than 0 and should be a number
			break
		else:
			# error message
			messagebox.showinfo("Error", "Please enter a valid CPU number (> 0)!")

	# return the entered value
	cpu_num = value

	# clear
	clear_widgets(root)

	return cpu_num

# ask whether the user wants to run_py at local
# local = 0 -> just end
# local = 1 -> local run
# for this purpose, there should be an independent TK created
def select_local(root):
	# create a new window
	#nowroot = create_root()
	var = tk.IntVar()
	var1 = tk.IntVar()
	# set the window bigger
	root.minsize(width=200, height=200)


	# default, local = 0
	local = 0

	# place two radio buttons
	Radiobutton(root ,text="End now",value=0,variable = var1).grid(row = 0,column = 0)
	Radiobutton(root,text="Run on local",value=1,variable = var1).grid(row = 1,column = 0)
	# set default (endnow)
	var1.set(0)

	# create button and set it to be ended
	button = tk.Button(root,text="Confirm", command = lambda:var.set(1))
	button.place(relx=.5, rely=.5, anchor="c")
	
	# button clicked
	button.wait_variable(var)
	# close the window
	#destroy_root(nowroot)
	local = var1.get()



	return local

# clear widgets for the next use
def all_children (window) :
	_list = window.winfo_children()
	for item in _list :
		if item.winfo_children() :
			_list.extend(item.winfo_children())

	return _list

def clear_widgets(root):
	widget_list = all_children(root)
	for item in widget_list:
		item.pack_forget()
	return 1