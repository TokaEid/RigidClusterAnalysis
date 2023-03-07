####
# This code extracts data from NoP_VF.txt files and plots the viscosity against the Mean/Median of the 
# maximum cluster sizes for all NoPs and all VFs
####

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import os, os.path

#To be used for plot legends later
colors = [[0.76, 0.77, 0.775, 0.78, 0.79, 0.8], ["deepskyblue", "blue", "blueviolet", "purple", "magenta", "crimson"]]
markers = [[500, 1024, 2000, 5000, 10000], ["X", "^", "o", "d", "s"]]

#Get a list of the all the files in current directory
files = os.listdir('.')
files.remove('plot_data_R.py')
files.sort()
nop = []
vf = []
k = 0

#Make a list of all the different VFs and NoPs present in the data
for file in files:
	file = file.split('_')
	nop_tmp = int(file[1])
	if not nop_tmp in nop:
		nop.append(nop_tmp)
	
	vf_tmp = float(file[2][2:-4])
	if not vf_tmp in vf:
		vf.append(vf_tmp)

#Only necessary to get data from rate controlled dir (Not very relevant for stress controlled analysis only)
###
mydir = os.getcwd()
mydir_tmp = mydir + "/../rateControlled"
mydir_new = os.chdir(mydir_tmp)

filesR = os.listdir('.')
filesR.sort()
filesR = filesR[2:-4]

os.chdir(mydir)
###

nop = np.sort(nop)
vf = np.sort(vf)

fig = plt.figure(1)
fig.set_size_inches(9,7.5)

#Plots all the data obtained from files (Viscosity vs Mean/Median Cluster Size for all VFs and NoPs)
for N in nop:
	for VF in vf:
		name = "N_" + str(N) + "_VF" + str(VF) + ".txt"
		stress = []
		visc = []
		std_visc = []
		mean_clus = []
		med_clus = []
		std_clus = []
		if name in files:
			with open(name) as myFile:
				myLines = myFile.readlines()
				for aline in myLines:
					#Append each element of the line to its proper array 
					aline = aline.split()
					stress.append(float(aline[0]))
					visc.append(float(aline[1]))
					std_visc.append(float(aline[2]))
					mean_clus.append(float(aline[3]))
					med_clus.append(float(aline[4]))
					std_clus.append(float(aline[5]))

				#Normalize arrays
				mean_clus = [x / N for x in mean_clus]
				med_clus = [x / N for x in med_clus]
				std_clus = [x / N for x in std_clus]
				
				#Assigning specific color and marker based on VF and NoP
				i = colors[0].index(VF)
				j = markers[0].index(N)

				#Rate controlled related
				###
				if N == 2000:
					nameR = "N_" + str(N) + "_VF" + str(VF)  + "_R.txt"
					os.chdir(mydir_tmp)
					viscR = []
					std_viscR = []
					mean_clusR = []
					med_clusR = []
					std_clusR = []
					if nameR in filesR:
						with open(nameR) as myFileR:
							myLinesR= myFileR.readlines()
							for lineR in myLinesR:
								lineR = lineR.split()
								viscR.append(float(lineR[0]))
								std_viscR.append(float(lineR[1]))
								mean_clusR.append(float(lineR[2]))
								med_clusR.append(float(lineR[3]))
								std_clusR.append(float(lineR[4]))

							plt.scatter(med_clusR, viscR, marker=markers[1][j], color=colors[1][i], edgecolors='black', label='Rate controlled')

							plt.errorbar(med_clusR, viscR, xerr=std_clusR, yerr=std_viscR, fmt='none', ecolor='black', elinewidth=0.2)

							plt.yscale('log')

					os.chdir(mydir)
				###

				#These will be used to make the legend, it's a very tedious way to do it but it was the first thing
				#I thought of
				patch0 = mpatches.Patch(color=colors[1][0], label=str(vf[0]))
				patch1 = mpatches.Patch(color=colors[1][1], label=str(vf[1]))
				patch2 = mpatches.Patch(color=colors[1][2], label=str(vf[2]))
				patch3 = mpatches.Patch(color=colors[1][3], label=str(vf[3]))
				patch4 = mpatches.Patch(color=colors[1][4], label=str(vf[4]))
				patch5 = mpatches.Patch(color=colors[1][5], label=str(vf[5]))

				mark0 = mlines.Line2D([],[], color='w', marker=markers[1][0], label=str(nop[0]), markerfacecolor='black', markersize=10)
				mark1 = mlines.Line2D([],[], color='w', marker=markers[1][1], label=str(nop[1]), markerfacecolor='black', markersize=10)
				mark2 = mlines.Line2D([],[], color='w', marker=markers[1][2], label=str(nop[2]), markerfacecolor='black', markersize=10)
				mark3 = mlines.Line2D([],[], color='w', marker=markers[1][3], label=str(nop[3]), markerfacecolor='black', markersize=10)
				mark4 = mlines.Line2D([],[], color='w', marker=markers[1][4], label=str(nop[4]), markerfacecolor='black', markersize=10)
				mark5 = mlines.Line2D([],[], color='w', marker=markers[1][2], label='Rate Controlled', markerfacecolor='white', markeredgecolor='black', markersize=10)

				#Making the actual plot
				#To plot Mean or Median, change the x array to mean_clus or med_clus respectively
  
				plt.scatter(mean_clus, visc, marker=markers[1][j], c=colors[1][i], label=VF)
				plt.errorbar(mean_clus, visc, xerr=std_clus, yerr=std_visc, fmt='none', ecolor='black', elinewidth=0.2)
				plt.yscale('log')
				plt.xlim(-0.2,1.2)
				Legend1 = plt.legend(handles=[patch0,patch1,patch2,patch3,patch4,patch5], title="Volume Fractions", loc='upper left')
				plt.gca().add_artist(Legend1)
				plt.legend(handles=[mark0,mark1,mark2,mark3,mark4,mark5], loc='lower right', title="Number of Particles")
				plt.xlabel('Mean of Maximum Cluster Sizes')
				plt.ylabel('Viscosity (Log)')


plt.show()
