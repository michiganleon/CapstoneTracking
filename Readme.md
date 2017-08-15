#Face Tracking based on KCF

**this project is implemented based on the python implementation of uoip from https://github.com/uoip/KCFpy**

Documents, videos, demos and some other results can be founded in following google drive link:
https://drive.google.com/drive/folders/0B1cwJfdr4A45WVdTZzhiMkk0RWM?usp=sharing

In this repo, 
- /DesignReview 主要是我们一些designreview的ppt,报告
- /kcf_py 是我们的模型的代码
- /kcf_master 是一个c++的kcf，最后没用

可以用/kcf_py下面的run.py来跑demo，
- 没有输入的话就是接摄像头，如果想处理video的话可以写python run.py videoname
- 默认输出实时视频，想保存的话看一下run.py里面有一些注释掉的代码，可以输出视频
- 默认是用dlib的detector 要用faster-rcnn的model的话需要安装好rcnn的库，（欢妹来补充一下怎么装你的model），然后改下kcftracker.py的7&109行附近的代码
- 使用前需要安装opencv，dlib等一些库，装dlib之前要装boost。具体安装有问题可以微信问我 huxuefeng1994
- 想开hog feature的话看一下run.py 34行左右的参数改一下
- master下面是我们最后demo的版本， new score的branch下面做了一个mix ranking的score function，理论上应该会让轨迹更顺滑但是跑得有点慢所以关掉了。供参考。
- 如果想显示轨迹的话，看一下run.py 94-104的code

有问题随时联系！