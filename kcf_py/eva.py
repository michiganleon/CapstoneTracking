import numpy as np 
import cv2
import sys
from time import time
import os
from os import listdir
from os.path import isdir,isfile, join
from numpy import loadtxt
import csv
import kcftracker


selectingObject = False
initTracking = False
onTracking = True
ix, iy, cx, cy = -1, -1, -1, -1
w, h = 0, 0
counter = 0
grace_period = 150
grace_counter = 0
detect_interval = 1
inteval = 1
duration = 0.01
scaleX = 1
scaleY = 1

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
	#if you use hog feature, there will be a short pause after you draw a first boundingbox, that is due to the use of Numba.
	detector = kcftracker.FRCNNDetector()
	tracking_pts = [] #list to store trajectory points, flush when tracking restart or reach 255 points
	for i in range(len(groundtruthes)):
		frame = cv2.imread(testcase_dir+"/"+imglist[i+offset])


		#print(testcase_dir+"/"+imglist[i+offset])
		counter = counter + 1
		if(counter%detect_interval == 0):
			detector.update(frame)

		boundingbox = []
		if(initTracking):
			if(counter%detect_interval == 0 and detector.exist_face()):
				boundingbox = detector.best_face()
				#print boundingbox
				tracker.init(boundingbox, frame)
				
				initTracking = False
				onTracking = True
			else:
				boundingbox = [0,0,0,0]

		elif(onTracking):
			boundingbox = tracker.update(frame)

			boundingbox = map(int, boundingbox)

			if(counter%detect_interval == 0 and (not detector.is_face(boundingbox))):
				if(detector.result_num > 0):
					print "re init with another face"
					grace_counter = 0
					boundingbox = detector.best_face()
					tracker.init(boundingbox, frame)
					#tracking_pts = []	
				elif(grace_counter < grace_period):
					print "grace period"
					grace_counter = grace_counter + 1
				else:
					print "re init seq"
					grace_counter = 0
					initTracking = True
					onTracking = False
					continue

		ratio = overlape_ratio(boundingbox, groundtruthes[i])
		print boundingbox
		print groundtruthes[i]
		result2.append([i, ratio])
		result.append(ratio)
		print ratio
		print "progress : " + str(float(i)/len(groundtruthes))
		cv2.rectangle(frame,(boundingbox[0],boundingbox[1]), (boundingbox[0]+boundingbox[2],boundingbox[1]+boundingbox[3]), (0,255,255), 1)
		px = boundingbox[0] + boundingbox[2]/2
		py = boundingbox[1] + boundingbox[3]/2

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

