from tkinter import *
from tkinter import filedialog
import shutil
import tkinter as tk
from tkinter import messagebox
import filediag as fd
import atexit
import os

import subprocess 

def bayes_select_ui():
	# select which task to do
	# 1. Bayesian correction?
	# 2. Bayesian meta-analysis?
	# according to the selection, change the current directory and run the relevant UI

	# create a window to get selection
	root = fd.create_root()

	# call the function
	nexts = get_next_task(root)

	# close the window
	fd.destroy_root(root)

	# run the selected task
	at_the_end(nexts)

	return 1

# what shall do next?
# if next = 1, then run Bayesian meta-analysis
# if not, then run Bayesian correction
def at_the_end(nexts):
	if (nexts == 0):
		# end and run
		# move to bayesian ui directory
		#os.chdir('Correction_UI')
		#atexit.register(lambda: exec(open('bayes_correction_ui.py').read()))
		subprocess.call(["python", "bayes_correction_ui.py"], cwd="Correction_UI")
	else:
		# run meta-analysis
		#os.chdir('Meta_UI')
		#atexit.register(lambda: exec(open('bmeta_ui.py').read()))
		subprocess.call(["python", "bmeta_ui.py"], cwd="Meta_UI")
	return 1

# A function to deal with the option selection
def get_next_task(root):
	# declare base variables
	var = tk.IntVar()
	var1 = tk.IntVar()

	# set the window bigger
	root.minsize(width=300, height=200)

	# show messagebox to let the user know what shall do
	messagebox.showinfo("Select task to do", "Please select which task you want to do next.")
	# present two radiobuttons
	Radiobutton(root ,text="Bayesian correction",value=0,variable = var1).grid(row = 0,column = 0)
	Radiobutton(root,text="Bayesian meta-analysis",value=1,variable = var1).grid(row = 1,column = 0)
	# set default (correction)
	var1.set(0)

	# create button and set it to be ended
	button = tk.Button(root,text="Next", command = lambda:var.set(1))
	button.place(relx=.5, rely=.5, anchor="c")

	# button clicked
	button.wait_variable(var)

	# close the window
	nexts = var1.get()

	# end the function
	return nexts

# if the current file is just called in the commandline, call the main function
bayes_select_ui()