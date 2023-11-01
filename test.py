# global cap_v4l.cpp:1119 tryIoctl VIDEOIO(V4L2:/dev/video0): select() timeout.
# sudo modprobe bcm2835-v4l2
# import cv2
from cv2 import cv2

camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
status, image = camera.read()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# Capture frame
ret, frame = cap.read()
if ret:
	cv2.imwrite('testimage.jpg', frame)

cap.release()
