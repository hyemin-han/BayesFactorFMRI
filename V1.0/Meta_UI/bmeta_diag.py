# dialogs specific for bmeta UI

# basically reuse functions in filediag.py
import filediag as fd
import os
import shutil

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# create Ns of filename presentation, N boxes and T/Z selection stuff
# get file list as input
# then return dataframe
# Filenames N Stat
def create_return_lines(root, filelist):
	# set the window bigger
	root.minsize(width=200, height=200)

	# filelist should be in list
	file_num = len(filelist)
	# get filenames without directories to be displayed
	pure_filenames = [None] * file_num
	for i in range(file_num):
		pure_filenames[i] = os.path.basename(filelist[i])
	# then create filename displayers, N textboxes, and radiobuttons "file_num" times
	filename_disp = [None] * file_num
	Nboxes = [None] * file_num
	Tradio = [None] * file_num
	Zradio = [None] * file_num
	var_stat = [None] * file_num
	Ns = [None]*file_num
	
	# for loop to create lines
	for i in range(file_num):
		# to get Z/T data from radiobuttons
		var_stat[i] = tk.IntVar()
		# filename displayer
		filename_disp[i]=tk.Label(root,text=pure_filenames[i]).grid(row=i+1,column=0)
		# NBox
		Nboxes[i] = tk.Entry(root, validate='key')
		Nboxes[i].grid(row = i+1,column = 1)
		# radioboxes Z / T
		Zradio[i] = tk.Radiobutton(root ,text="Z",value=0,variable = var_stat[i]).grid(row = i+1,column = 2)
		Tradio[i] = tk.Radiobutton(root ,text="T",value=1,variable = var_stat[i]).grid(row = i+1,column = 3)
		# default = z
		var_stat[i].set(0)

	# last: confirm button
	var_confirm = tk.IntVar()
	button = tk.Button(root,text="Confirm", command = lambda:var_confirm.set(1))
	button.grid(row=file_num+2,column=1)

	# value check. whether valid Ns were entered.
	# while loop...
	# wait until we get a correct int value > 0
	while(1):
		# button clicked
		button.wait_variable(var_confirm)

		# get input
		for i in range(file_num):
			Ns[i] = Nboxes[i].get()
		# check the validation func
		flag = check_N(Ns)

		if flag == 1:
			break
		else:
			# error message
			messagebox.showinfo("Error", "Please enter N number (> 0)!")
	# convert z/t into list
	stats=[None]*file_num
	for i in range(file_num):
		# get radio button values
		var_stat[i]= var_stat[i].get()
		if (var_stat[i] == 0):
			stats[i]='Z'
		elif (var_stat[i]==1):
			stats[i]='T'
	# dictionary of lists
	dict = {'Filename':filelist, 'N': Ns, 'Type': stats}
	# create dataframe
	df = pd.DataFrame(dict)
	return df

# check whether valid Ns were entered
def check_N(vars):
	flag = 1
	# get the length of vars
	N_num = len(vars)
	# detect if there is any invalid value
	for i in range(N_num):
		# num?
		if (vars[i].isnumeric() == False):
			# invalid text
			flag = 0
			break
		# zero > N ?
		if ((int(vars[i])<=0)):
			# negative or zero value
			flag = 0
			break
	return flag

# save df into csv
def save_df(workingdir, df):
	# save into working dir
	df.to_csv(workingdir+'/list_original.csv',index=False)
	return 1


def copy_all_files_meta(workingdir,ddf):
	# define the list of required source files	
	# first, python codes
	py_list = ['bmeta_main.py','bmeta_modlist.py','bmeta_split.py','convert_nii.py','threshold.py']
	# get the number of py files
	py_num = len(py_list)
	# then, R files
	R_list = ['fmri_bmeta_random1.R','integrate_result.R','integrate_result_minus.R','config.csv']
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

	# copy image files based on ddf
	# and then conver to the current folder
	files = ddf.Filename
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
		# plus, change the content in ddf
		ddf.Filename[i] = pure_filenames[i]
	# then save to list.csv
	ddf.to_csv(workingdir+'/list.csv',index=False)


	return 1