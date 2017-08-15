import numpy as np 
import cv2
import sys
from time import time

import kcftracker

	#detector box, tracker box
	def overlape_ratio(self,box1,box2):
		#print box1
		#print box2
		x_overlap = float(box1[2] + box2[2] - (max(box1[0]+box1[2],box2[0]+box2[2]) - min(box1[0],box2[0])))
		y_overlap = float(box1[3] + box2[3] - (max(box1[1]+box1[3],box2[1]+box2[3]) - min(box1[1],box2[1])))
		if(x_overlap < 0): 
			x_overlap = 0
		if(y_overlap < 0): 
			y_overlap = 0
		ratio = (x_overlap * y_overlap) / (float(box1[2]) * float(box1[3]) + float(box2[2]) * float(box2[3]))
		#print ratio
		return ratio



tracker = kcftracker.KCFTracker(False, True, True)  # hog, fixed_window, multiscale

	while(cap.isOpened()):
		ret, frame = cap.read()
		if not ret:
			break

		if(selectingObject):
			cv2.rectangle(frame,(ix,iy), (cx,cy), (0,255,255), 1)
		elif(initTracking):
			cv2.rectangle(frame,(ix,iy), (ix+w,iy+h), (0,255,255), 2)

			tracker.init([ix,iy,w,h], frame)

			initTracking = False
			onTracking = True
		elif(onTracking):
			t0 = time()
			boundingbox = tracker.update(frame)
			t1 = time()

			boundingbox = map(int, boundingbox)
			cv2.rectangle(frame,(boundingbox[0],boundingbox[1]), (boundingbox[0]+boundingbox[2],boundingbox[1]+boundingbox[3]), (0,255,255), 1)
			
			duration = 0.8*duration + 0.2*(t1-t0)
			#duration = t1-t0
			cv2.putText(frame, 'FPS: '+str(1/duration)[:4].strip('.'), (8,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

		cv2.imshow('tracking', frame)
		c = cv2.waitKey(inteval) & 0xFF
		if c==27 or c==ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()
