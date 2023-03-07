####
# This code works by going through every time step directory produced by the pebble game and extracts the rigid clusters formed for each one
# and then saves the maximum, mean and median of each time frame and saves all this data in a text file. 
#
# This code needs to be located in the same directory as the N_dirs
# Adjust the input number of particles, friction, and volume fraction in the input section in the beginning
####

import numpy as np
import os, sys
import glob
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from string import digits
import statistics as stat

## INPUT
#Choose the NoP, friction, and particular Volume fraction you want to run the code on
N = ["N_2000"]
mu = ["mu_0.5"]
VF = ["VF0.8"]
##

#Change directory according to input path
mydir = os.getcwd()
for n in N:
	for m in mu:
		for vf in VF:
			mydir_tmp = mydir + "/" + n + "/" + m + "/" + vf
			mydir_new = os.chdir(mydir_tmp)
			
			#Gets list of subdirectories in current directory (The Stress Directories)
			d = '.'
			subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
					
			#To be used later
			num_stress = len(subdirs)
			i = 0
			length = -1
			mx = -1
			mn = -1
			md = -1

			#Extracts all directories and files in the folder root
			for root, dirs, files in os.walk("."):
			
				#Saving the stress for later use
				if len(root)>1:
					st = root[1:]
					st = st.split('/')[1]

				#Resetting the arrays to zeros every time we encounter a new directory (new stress)
				if dirs and len(dirs)>num_stress:
					length = len(dirs)
					i = 0
					time = np.empty(length)
					maxcl = np.zeros(length)
					meancl = np.zeros(length)
					mediancl = np.zeros(length)

				#Making sure the code only runs for the time directories that have the output.log files
				if root and (not dirs):
					#Nroot is the value of the time step
					nroot = root[1:]
					nroot = nroot.split('/')[2]
						
					#Outputs time array 
					time[i] = "{:.2f}".format(float(nroot))		
			
					#To find the cluster size in the output.log file:
					location = root
					index = -1
					lookup = 'Cluster sizes (particles)'
					with open(os.path.join(location,'output.log'),"r") as myData:
						for num, line in enumerate(myData,1):
							if lookup in line:
								index = num+1
				
							if num == index:
								#Editing the string to easily convert it to a list
								#(There's probably a simpler way to do this, I just
								#didn't worry too much about it since it worked)
								l = int(len(line)) - 2
								line = line[1:l]
								line = line.replace(" ","")
								line = line.split(',')
								line = [item.replace(" ","") for item in line]
								for j in range(0, len(line)):
									if line[j]:
										line[j] = int(line[j])
									else:
										line[j] = 0

								#Collecting the maximum/mean/median sizes in an array
								mx = max(line)
								maxcl[i] = "{:.3f}".format(mx)
								mn = stat.mean(line)
								meancl[i] = "{:.3f}".format(mn)
								md = stat.median(line)
								mediancl[i] = "{:.3f}".format(md)
					i+=1

				#Every time we've ran through all the time snapshots,
				#we save the maxcl/Meancl/Mediancl arrays before moving on to a new
				#stress directory and starting all over again
				if i==length:
					#Sorting Maxcl/Meancl/Mediancl based on Sorted Time Array
					inds = time.argsort()
					maxcl = maxcl[inds]
					meancl = meancl[inds]
					mediancl = mediancl[inds]
					time = sorted(time)

					#Save arrays in text file in each stress dir
					output1 = np.stack((time,meancl,mediancl,maxcl), axis=1)
					filename1 = "./clusterSizes_" + st + ".txt"
					file1 = open(filename1,"w")
					np.savetxt(file1, output1, fmt='%.2f')
					file1.close()	
		
#Resetting the current directory
os.chdir(mydir)	
