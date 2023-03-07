####
# This code works by going through every time step directory produced by the pebble game and extracts the rigid clusters formed for each one
# and then plots the probability distribution of the cluster sizes for each stress
#
# This code needs to be located in the same directory as the N_dirs
# Adjust the input number of particles, friction, and volume fraction in the input section in the beginning
####

import numpy as np
import os, sys
import glob
import io
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib import colors as mcolors
from matplotlib.backends.backend_pdf import PdfPages
from string import digits
import statistics as stat


## INPUT
#Choose the NoP, friction, and particular Volume fraction you want to run the code on
N = ["N_2000"]
mu = ["mu_1"]
VF = ["VF0.78"]
##


#Change directory according to input path		
mydir = os.getcwd()
mydir_tmp = mydir + "/" + N[0] + "/" + mu[0] + "/" + VF[0]
mydir_new = os.chdir(mydir_tmp)


#Gets list of subdirectories in current directory (The Stress Directories)
d = '.'
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

					
#To be used later
num_stress = len(subdirs)
i = 0
length = -1
norm = int(N[0][2:])
zs = [10,20,40,50,80,100]
total_clus = []
for m in range(len(zs)):
	total_clus.append([])


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
							line[j] = int(line[j])/norm
						else:
							line[j] = 0

					if (int(st) in zs):
						idx = zs.index(int(st))
						total_clus[idx].append(line[0])

		i+=1

fig = plt.figure()
ax = fig.gca(projection='3d')

kwargs = dict(alpha=0.5,bins=100,density=True,stacked=True)

def cc(arg):
	return mcolors.to_rgba(arg, alpha=0.7)

verts = []
for z in range(len(zs)):
	count, bins, patches = ax.hist(total_clus[z], **kwargs)
	xs = np.append(np.repeat(bins,2)[1:],0)
	ys = np.append(np.repeat(count,2),[0,0])
	verts.append(list(zip(xs,ys)))

plt.cla()

poly = PolyCollection(verts, facecolors=[cc('r'), cc('orange'), cc('y'), cc('g'), cc('b'), cc('purple')])

poly.set_alpha(0.7)
ax.add_collection3d(poly, zs=zs, zdir='y')

#ax.set_axis_off()
ax.grid(False)

ax.set_xlabel('Cluster Size')
ax.set_xlim3d(0,1)
ax.set_ylabel('Stress')
ax.set_ylim3d(2,100)
ax.set_zlabel('Prob Distrib')
ax.set_zlim3d(0,20)

plt.show()


#Resetting the current directory
os.chdir(mydir)	
