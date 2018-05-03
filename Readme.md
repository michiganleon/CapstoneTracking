Face Tracking based on KCF
==========================

**this project is implemented based on the python implementation of uoip from https://github.com/uoip/KCFpy**

Documents, videos, demos and some other results can be founded in following google drive link:
https://drive.google.com/drive/folders/0B1cwJfdr4A45WVdTZzhiMkk0RWM?usp=sharing

In this repo, 
-（+*）  /DesignReview includes the reports
-（+*）  /kcf_py includes the src of the project
-（+*）  /kcf_master a c++ version kcf. 

**可以用/kcf_py下面的run.py来跑demo，

-（+*）  Usage: python run.py will connect to the camera, and python run.py filename will use video file as input
-（+*）  by default using dlib detector. Install RCNN lib and modify kcftracker.py line 7 & 109 to use RCNN dector.
-（+*）  check run.py line 34 for hog features
-（+*）  check branch: mix-ranking for an alternative score function.
-（+*）  check run.py line 94-104 to show trajectory. 

Contact: leonhuxf@umich.edu
