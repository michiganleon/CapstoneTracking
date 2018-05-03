Face Tracking based on KCF
==========================

**this project is implemented based on the python implementation of uoip from https://github.com/uoip/KCFpy**

Documents, videos, demos and some other results can be founded in following google drive link:
https://drive.google.com/drive/folders/0B1cwJfdr4A45WVdTZzhiMkk0RWM?usp=sharing

In this repo, 
1.  /DesignReview includes the reports
2.  /kcf_py includes the src of the project
3.  /kcf_master a c++ version kcf. 

**可以用/kcf_py下面的run.py来跑demo，

1.  Usage: python run.py will connect to the camera, and python run.py filename will use video file as input 
2.  by default using dlib detector. Install RCNN lib and modify kcftracker.py line 7 & 109 to use RCNN dector.
3.  check run.py line 34 for hog features 
4.  check branch: mix-ranking for an alternative score function.
5.  check run.py line 94-104 to show trajectory. 

Contact: leonhuxf@umich.edu
