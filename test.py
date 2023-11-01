import pytesseract
from pytesseract import Output
from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Initialize PiCamera
camera = Picamera2()

# Set camera resolution (adjust these values as needed)
camera.resolution = (1280, 720)
capture_config = camera.create_still_configuration()
camera.start()

while True:
    # Capture a frame from the camera feed
    frame = camera.capture_frame()

    # Display the live feed in a window
    cv2.imshow('Camera Feed', frame)

    # Wait for user input and capture an image if 'p' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('p'):
        # Capture an image and save it to a file
        camera.capture_file("image.jpg")
        break

# When everything is done, release the camera and close the windows
camera.close()
cv2.destroyAllWindows()

# Read the captured image from file
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
