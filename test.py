# sudo modprobe bcm2835-v4l2
import cv2

cap = cv2.VideoCapture(0)

# Capture frame
ret, frame = cap.read()
if ret:
	cv2.imwrite('testimage.jpg', frame)

cap.release()
