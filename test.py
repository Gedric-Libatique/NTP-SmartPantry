import pytesseract
from pytesseract import Output
from picamera2 import Picamera2, Preview
import numpy as np
import cv2
import time
import keyboard

camera = Picamera2()
camera_config = camera.create_preview_configuration()
camera.configure(camera_config)
camera.start_preview(Preview.QTGL)
camera.start()

while True:
    # Wait for user input and capture an image if 'p' is pressed
    if keyboard.is_pressed('p'):
        # Capture an image and save it to a file
        camera.capture_file("image.jpg")
        break

# When everything is done, release the camera and close the windows
camera.close()
time.sleep(2)
frame = cv2.imread('image.jpg')

d = pytesseract.image_to_data(frame, output_type=Output.DICT)
n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        # don't show empty text
        if text and text.strip() != "":
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

# Display the resulting frame
cv2.imshow('frame', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
