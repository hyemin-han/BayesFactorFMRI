import os
import pandas as pd

def bayes_correction_modlist(list):
	# modify the list
	# then create list_mod.csv

	lists = pd.read_csv(list)

	# new file name should be list_mod
	filename = os.path.splitext(list)[0]
	#filename = os.path.split(filename)[1]
	newfilename = filename+"_mod.csv"


	# then get the path of list
	if (os.path.split((list))[0] != ''):
		path = os.path.split(os.path.abspath(list))[0]+"/"
	else:
		path = os.path.split((list))[0]


	# modify pandas dataframe
	lists["Filename"] = path+lists["Filename"]

	# save list_mod.csv
	# in the current directory
	lists.to_csv(newfilename, index=False)

	# return new filename
	return (newfilename)