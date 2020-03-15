import os
import pandas as pd

def bmeta_modlist(list):
	# modify the list
	# then create list_mod.csv

	lists = pd.read_csv(list)

	filecount = len(lists.Filename)

	# new file name should be list_mod
	filename = os.path.splitext(list)[0]
	#filename = os.path.split(filename)[1]
	newfilename = filename+"_mod.csv"

	# then loop
	for x in range(0,filecount):
		lists.Filename[x] = './transformed/'+lists.Filename[x]

	# save list_mod.csv
	# in the current directory
	lists.to_csv(newfilename, index=False)

	# return new filename
	return (newfilename)