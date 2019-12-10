# hikvision_camera
海康威视-网络摄像头录像及截图

## 依赖  
基于cv2  
```python
pip install opencv-python
```

## 参数  
根据conf/conf.ini中的配置，修改正确的ip及用户名密码等信息  

## 调试  
通过main.py，预设了2个function，一个是控制截屏、一个是录制视频10秒钟；
输出保存的位置为./logs/camera_img/中