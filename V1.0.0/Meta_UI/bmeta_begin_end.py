# dealing with the beginning to the end of bmeta UI

import os
import bayes_correction_begin_end as bcbe

# create run this
def bmeta_run_this(workingdir,cpu_num,minus = 0):
	# the format will be
	# from bmeta_main import bmeta_main

	# create text contents
	line1 = "from bmeta_main import bmeta_main\r\n"
	line2 = "bmeta_main(\"list.csv\","+str(cpu_num)+","+str(minus)+")\r\n"

	# write into run_this.py
	outF = open(workingdir+"/run_this.py", "w")
	outF.write(line1)
	outF.write(line2)

	return 1

# run the current runthis after the end of bmeta UI
def run_now(workingdir):
	# call the one in bcbe for efficiency
	bcbe.run_now(workingdir)
	return 1