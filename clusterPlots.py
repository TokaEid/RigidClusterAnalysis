####
# This code extracts the cluster data from the clusterSizes text files and plots two things:
# 1. A return map for all the stresses in a specific volume fraction
# 2. A time-lapse of the max_cluster distribution
#
# This code needs to be located in the same directory as the N_ dirs
# Scroll to the bottom to adjust input number of particles, friction, and volume fraction
####


import numpy as np
import os
import statistics as stat
import matplotlib.pyplot as plt
import matplotlib.colors

class clusterPlots:

	def __init__(self, N, mu, VF):
		
		self.N = N[0]
		self.mu = mu[0]
		self.VF = VF[0]

		#Change dir according to input path
		mydir = os.getcwd()
		mydir_tmp = mydir + "/" + self.N + "/" + self.mu + "/" + self.VF
		mydir_new = os.chdir(mydir_tmp)

		d = '.'
		subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
		for i in range(len(subdirs)):
			subdirs[i] = int(subdirs[i][2:]) 			

		#To be Used Later
		self.stresses = subdirs
		self.stresses = sorted(self.stresses, reverse=True)
		self.stresses = self.stresses[:-2]

		cmap = plt.cm.jet
		color_theme = cmap(np.linspace(0,1,9))
		color1 = color_theme[0,:]
		color2 = color_theme[2,:]
		color3 = color_theme[6,:]
		color4 = color_theme[7,:]
		color5 = color_theme[8,:]
		color_scale = [[5, 10, 20, 50, 100], [color1, color2, color3, color4, color5]]

		fig = plt.figure(1)
		fig.set_size_inches(8,8)

		# (1) Extract cluster info from text files and plots return map
		for stress in self.stresses:
			filenameC = "clusterSizes_" + str(stress) + ".txt"
			max_clus = []
			with open(filenameC, "r") as fileC:
				lines = fileC.readlines()
				for lineC in lines:
					lineC = lineC.split()
					max_clus.append(float(lineC[3]))

			max_clus = max_clus[4:]
			norm = int(self.N[2:])
			max_clus = [element/norm for element in max_clus]

			xn = max_clus
			xn1 = max_clus[1:]
			xn = max_clus[:-1]

			i = color_scale[0].index(int(stress))

			plt.scatter(xn, xn1, s=5, c=color_scale[1][i], label = '$\sigma$ = ' + str(stress))
			plt.xlabel("S$_{max,i}$", fontsize=20)
			plt.ylabel("S$_{max,i+1}$", fontsize=20)
			plt.xlim(-0.05,1)
			plt.ylim(-0.05,1)
			plt.legend(loc=4, bbox_to_anchor=(1,0.5), fontsize=14)


		fig2 = plt.figure(2)
		fig2.set_size_inches(10,6)

		# (2) Extracts cluster info from text files and plots time distribution
		for stress in self.stresses:
			filenameC = "clusterSizes_" + str(stress) + ".txt"
			max_clus = []
			time = []
			with open(filenameC, "r") as fileC:
				lines = fileC.readlines()
				for lineC in lines:
					lineC = lineC.split()
					time.append(float(lineC[0]))
					max_clus.append(float(lineC[3]))

			max_clus = max_clus[4:]
			time = time[4:]
			norm = int(self.N[2:])
			max_clus = [element/norm for element in max_clus]

			j = color_theme[0].index(int(stress))

			plt.scatter(time, max_clus, s=10, c=color_theme[1][j], label=str(stress))
			plt.ylim(0,1)
			plt.legend(loc = 7, bbox_to_anchor=(1.05,0.5), title="Stresses at" + self.VF)
			plt.xlabel("Time")
			plt.ylabel("Max Cluster Size")
 
		plt.show()
		
		#Reset current dir
		os.chdir(mydir)


#Choose NoP, friction, and volume fraction that you want to run the code for
n = ["N_2000"]
m = ["mu_1"]
f = ["VF0.79"]
cP = clusterPlots(n,m,f)
