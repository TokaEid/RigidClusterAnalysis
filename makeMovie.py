import cv2
import os, sys
import numpy as np
import glob
from natsort import natsorted

files = os.listdir('./Images')
files = natsorted(files)

img_array = []
for filename in files:
	filename = "./Images/" + filename
	img = cv2.imread(filename)
	height, width, layers = img.shape
	size = (width, height)
	img_array.append(img)

out = cv2.VideoWriter('myVid.avi', cv2.VideoWriter_fourcc(*'XVID'), 4, size)

for i in range(len(img_array)):
	out.write(img_array[i])
out.release()

