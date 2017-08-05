import sys
import dlib
import cv2

class detector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.result = []
        self.compress_factor = 0.25

    def detect(self, img):
        img = cv2.resize(img, (0,0), fx=self.compress_factor, fy=self.compress_factor)
        dets, scores, idx = self.detector.run(img, 1, -0.5)
        for i, d in enumerate(dets):
            self.result.append([dlib.rectangle.left(d)/self.compress_factor, dlib.rectangle.top(d)/self.compress_factor, 
                             dlib.rectangle.right(d)/self.compress_factor, dlib.rectangle.bottom(d)/self.compress_factor, scores[i]])
        # print self.result
        return self.result
