import numpy as np 
import cv2
import sys
from time import time

import kcftracker

selectingObject = False
initTracking = True
onTracking = False
ix, iy, cx, cy = -1, -1, -1, -1
w, h = 0, 0
counter = 0
grace_period = 50
grace_counter = 0
detect_interval = 1

inteval = 1
duration = 0.01

#fourcc = cv2.cv.CV_FOURCC(*'XVID')
#out = cv2.VideoWriter('output.avi', fourcc, 25.0, (720,1280))

# mouse callback function
def draw_boundingbox(event, x, y, flags, param):
	global selectingObject, initTracking, onTracking, ix, iy, cx,cy, w, h
	
	if event == cv2.EVENT_LBUTTONDOWN:
		selectingObject = True
		onTracking = False
		ix, iy = x, y
		cx, cy = x, y
	
	elif event == cv2.EVENT_MOUSEMOVE:
		cx, cy = x, y
	
	elif event == cv2.EVENT_LBUTTONUP:
		selectingObject = False
		if(abs(x-ix)>10 and abs(y-iy)>10):
			w, h = abs(x - ix), abs(y - iy)
			ix, iy = min(x, ix), min(y, iy)
			initTracking = True
		else:
			onTracking = False
	
	elif event == cv2.EVENT_RBUTTONDOWN:
		onTracking = False
		if(w>0):
			ix, iy = x-w/2, y-h/2
			initTracking = True



if __name__ == '__main__':
	
	if(len(sys.argv)==1):
		cap = cv2.VideoCapture(0)
	elif(len(sys.argv)==2):
		if(sys.argv[1].isdigit()):  # True if sys.argv[1] is str of a nonnegative integer
			cap = cv2.VideoCapture(int(sys.argv[1]))
		else:
			cap = cv2.VideoCapture(sys.argv[1])
			inteval = 30
	else:  assert(0), "too many arguments"


	tracker = kcftracker.KCFTracker(False, False, True)  # hog, fixed_window, multiscale
	#if you use hog feature, there will be a short pause after you draw a first boundingbox, that is due to the use of Numba.
	detector = kcftracker.FRCNNDetector()
	
	#w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
	#h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
	#fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
	#out = cv2.VideoWriter('output.mp4', fourcc, 25.0, (w,h))

	cv2.namedWindow('tracking')
	#cv2.setMouseCallback('tracking',draw_boundingbox)

	tracking_pts = [] #list to store trajectory points, flush when tracking restart or reach 255 points
	while(cap.isOpened()):
		ret, frame = cap.read()
		if not ret:
			break

		counter = counter + 1
		if(counter%detect_interval == 0):
			detector.update(frame)

		if(initTracking):
			if(counter%detect_interval == 0 and detector.exist_face()):
				tracker.init(detector.best_face(), frame)
				initTracking = False
				onTracking = True

		elif(onTracking):
			t0 = time()
			boundingbox = tracker.update(frame)
			t1 = time()

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

			cv2.rectangle(frame,(boundingbox[0],boundingbox[1]), (boundingbox[0]+boundingbox[2],boundingbox[1]+boundingbox[3]), (0,255,255), 1)
			px = boundingbox[0] + boundingbox[2]/2
			py = boundingbox[1] + boundingbox[3]/2
#			tracking_pts.insert(0,(px,py))
#			pos = tracking_pts[0]
#			for i in range(0,len(tracking_pts)):
#				cv2.circle(frame,tracking_pts[i],10-(i/25),(255,i,i),(10-(i/25))/2)
#				if (i==0):
#					continue
#				cv2.line(frame,pos,tracking_pts[i],(255,255,255))
#				pos = tracking_pts[i]
#			if len(tracking_pts) >= 255:
#				tracking_pts.pop(254)
			duration = 0.8*duration + 0.2*(t1-t0)
			duration = t1-t0
			cv2.putText(frame, 'FPS: '+str(1/duration)[:4].strip('.'), (8,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

		cv2.imshow('tracking', frame)
		#out.write(frame)
		c = cv2.waitKey(inteval) & 0xFF
		if c==27 or c==ord('q'):
			break

	cap.release()
	out.release()
	cv2.destroyAllWindows()
