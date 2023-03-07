####
# This code extracts the cluster data from the clusterSizes file and plots a probability distribution 
# 
# This code should be placed in the same directory as the clusterSizes files
####

import numpy as np
import os, sys
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(color_codes=True)
sns.set(rc={'figure.figsize':(8,6)})

#Adjust NoP value and stress value here
filename = "clusterSizes_3.txt"
N = 5000

mean_clus = [] #Column number 1 in text file
med_clus = []  #Column number 2
max_clus = []  #Column number 3

with open(filename, "r") as file:
	lines = file.readlines()
	for line in lines:
		line = line.split()
		temp = float(line[1])/N
		mean_clus.append(temp)

stress = filename[13:-4]

fig = plt.figure(1)
fig.set_size_inches(10,8)
ax = sns.distplot(mean_clus, bins=np.arange(0,1.05,0.05), kde=True, kde_kws={'bw':0.02}, color='blue')
ax.set(xlabel='Mean Cluster Size', ylabel='Probability Distribution')
ax.set_xlim(-0.1,1)
ax.set_title(stress)

plt.show()
