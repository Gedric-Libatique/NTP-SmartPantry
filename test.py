File "/home/team4pi/Documents/pantry/test3.py", line 11, in <module>
    cv2.imshow('Live Video', frame)
cv2.error: OpenCV(4.8.1) /io/opencv/modules/highgui/src/window.cpp:971: error: (-215:Assertion failed) size.width>0 && size.height>0 in function 'imshow'

# sudo modprobe bcm2835-v4l2
import cv2

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Live Video', frame)

    # Break the loop on 'Q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
