####
# This code works to extract the viscosities from the data_ files and saves the mean viscosities for each stress
# as well as extract the relevant cluster data from the clusterSizes_(stress) text files. 
#
# This code needs to be located in the same directory as the N_ dirs
# Scroll to the bottom to adjust input number of particles, friction, and volume fraction
####


import numpy as np
import os
import statistics as stat

class makeDataFiles:

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
		self.stresses = sorted(self.stresses)
		rows = len(self.stresses)

		self.mean_visc = np.zeros(rows)
		self.med_visc = np.zeros(rows)
		self.std_visc = np.zeros(rows)
		self.mean_of_max_clus_size = np.zeros(rows)
		self.mean_of_mean_clus_size = np.zeros(rows)
		self.mean_of_med_clus_size = np.zeros(rows)
		self.med_of_max_clus_size = np.zeros(rows)
		self.med_of_mean_clus_size = np.zeros(rows)
		self.med_of_med_clus_size = np.zeros(rows)
		self.std_of_max_clus  = np.zeros(rows)
		self.std_of_mean_clus  = np.zeros(rows)
		self.std_of_med_clus  = np.zeros(rows)
		k=0

		#Extract Mean Viscosity from data_ files
		for stress in self.stresses:
			filenameV = "data_D2N" + self.N[2:] + self.VF + "Bidi1.4_0.5Square_1_pardata_phi" + self.VF[2:] + "_stress" + str(stress) + "cl.dat"
			self.visc=[]
			with open(filenameV,"r") as fileV:
				for line in fileV:
					if len(line)>100:
						line = line.split(' ')
						self.visc.append(float(line[4]))
			
			self.visc = [element for element in self.visc if element > 0]
			self.visc = [element for element in self.visc if element < 150000]

            
#Uncomment following block if you want to plot a viscosity distribution for a specific stress
"""
			if str(stress) == '100':
				import matplotlib.pyplot as plt
				import seaborn as sns
	
				sns.set(color_codes=True)
				sns.set(rc={'figure.figsize':(8,6)})

				peak = stat.mean(self.visc)
				add_text = 'Mean Viscosity = ' + str(peak)
				print(add_text)

				fig = plt.figure(1)
				fig.set_size_inches(10,8)
				ax = sns.distplot(self.visc, kde=True, color='blue')
				ax = sns.distplot(self.visc, bins=np.arange(0,150000,15000), kde=True, color='blue')
				ax.set(xlabel='Viscosity', ylabel='Probability Distribution')
				ax.set_xlim(-2000,150000)

				plt.show()
"""

			#Average viscosity and get standard deviation for each stress
			self.mean_visc[k] = stat.mean(self.visc)
			self.mean_visc[k] = np.around(self.mean_visc[k], decimals=3, out=None)

			self.med_visc[k] = stat.median(self.visc)
			self.med_visc[k] = np.around(self.med_visc[k], decimals=3, out=None)
			
			self.std_visc[k] = stat.stdev(self.visc)
			self.std_visc[k] = np.around(self.std_visc[k], decimals=3, out=None)

			#Extract cluster info from text files
			filenameC = "clusterSizes_" + str(stress) + ".txt"
			max_clus = []
			mean_clus = []
			med_clus = []
			with open(filenameC, "r") as fileC:
				lines = fileC.readlines()
				for lineC in lines:
					lineC = lineC.split()
					mean_clus.append(float(lineC[1]))
					med_clus.append(float(lineC[2]))
					max_clus.append(float(lineC[3]))

			mean_clus = mean_clus[4:]
			med_clus = med_clus[4:]
			max_clus = max_clus[4:]

			#Extracting the Mean of the previous three arrays (mean, med and max cluster sizes)
			self.mean_of_mean_clus_size[k] = stat.mean(mean_clus)
			self.mean_of_mean_clus_size[k] = np.around(self.mean_of_mean_clus_size[k], decimals=3, out=None)

			self.mean_of_med_clus_size[k] = stat.mean(med_clus)
			self.mean_of_med_clus_size[k] = np.around(self.mean_of_med_clus_size[k], decimals=3, out=None)

			self.mean_of_max_clus_size[k] = stat.mean(max_clus)
			self.mean_of_max_clus_size[k] = np.around(self.mean_of_max_clus_size[k], decimals=3, out=None)

			#Extracting the Median of the previous three arrays (mean, med and max cluster sizes)
			self.med_of_mean_clus_size[k] = stat.median(mean_clus)
			self.med_of_mean_clus_size[k] = np.around(self.med_of_mean_clus_size[k], decimals=3, out=None)

			self.med_of_med_clus_size[k] = stat.median(med_clus)
			self.med_of_med_clus_size[k] = np.around(self.med_of_med_clus_size[k], decimals=3, out=None)

			self.med_of_max_clus_size[k] = stat.median(max_clus)
			self.med_of_max_clus_size[k] = np.around(self.med_of_max_clus_size[k], decimals=3, out=None)

			#Extracting the standard deviation of the previous three arrays (mean, med and max cluster sizes)
			self.std_of_mean_clus[k] = stat.stdev(mean_clus)
			self.std_of_mean_clus[k] = np.around(self.std_of_mean_clus[k], decimals=3, out=None) 

			self.std_of_med_clus[k] = stat.stdev(med_clus)
			self.std_of_med_clus[k] = np.around(self.std_of_med_clus[k], decimals=3, out=None) 

			self.std_of_max_clus[k] = stat.stdev(max_clus)
			self.std_of_max_clus[k] = np.around(self.std_of_max_clus[k], decimals=3, out=None) 

			k+=1

		#Reset current dir
		os.chdir(mydir)


#Choose NoP, friction, and volume fraction that you want to run the code for
n = ["N_5000"]
m = ["mu_1"]
f = ["VF0.8"]
mDF = makeDataFiles(n,m,f)
