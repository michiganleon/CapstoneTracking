import numpy as np 
import cv2
import sys
import os
from os import listdir
from time import time
from os.path import isdir,isfile, join
from numpy import loadtxt
import csv
import kcftracker

#detector box, tracker box
def overlape_ratio(box1,box2):
	#print box1
	#print box2
	x_overlap = float(box1[2] + box2[2] - (max(box1[0]+box1[2],box2[0]+box2[2]) - min(box1[0],box2[0])))
	y_overlap = float(box1[3] + box2[3] - (max(box1[1]+box1[3],box2[1]+box2[3]) - min(box1[1],box2[1])))
	if(x_overlap < 0): 
		x_overlap = 0
	if(y_overlap < 0): 
		y_overlap = 0
	ratio = (x_overlap * y_overlap) / min((float(box2[2]) * float(box2[3])), (float(box1[2]) * float(box1[3])))
	#print ratio
	return ratio

if __name__ == '__main__':
	#cuurrent_dir = os.getcwd()
	if(len(sys.argv)==2):	
		testcase_dir = os.getcwd() + "/benchmark/"+sys.argv[1]+"/img"
	else:
		assert(0), "wrong arguments"

	imglist = [f for f in listdir(testcase_dir) if isfile(join(testcase_dir, f))]
	groundtruthes = []
	with open(os.getcwd() + "/benchmark/"+sys.argv[1]+"/groundtruth_rect.txt") as f:
		for line in f:
			inner_list = [int(elt.strip()) for elt in line.split(',')]
			groundtruthes.append(inner_list)
	#print groundtruthes
	result = []
	result2 = []

	offset = len(imglist) - len(groundtruthes)

	tracker = kcftracker.KCFTracker(True, True, True)  # hog, fixed_window, multiscale
	frame = cv2.imread(testcase_dir+"/"+imglist[offset])
	tracker.init(groundtruthes[0], frame)

	for i in range(len(groundtruthes)):
		frame = cv2.imread(testcase_dir+"/"+imglist[i+offset])
		#print np.shape(frame)
		boundingbox = tracker.update(frame)
		result2.append([i, overlape_ratio(boundingbox, groundtruthes[i])])
		result.append(overlape_ratio(boundingbox, groundtruthes[i]))

	with open(sys.argv[1]+"overlaprate.csv", 'wb') as myfile:
	    wr = csv.writer(myfile)
	    wr.writerows(result2)

	result = sorted(result)
	percentile = []
	for i in range(len(result)):
		perc = 1 - float(i)/float(len(result))
		percentile.append([result[i], perc])

	with open(sys.argv[1]+"successrate.csv", 'wb') as myfile:
	    wr = csv.writer(myfile)
	    wr.writerows(percentile)
	#
	#

