import pytesseract
from pytesseract import Output
from picamera import PiCamera
import cv2
import numpy as np
import time

# Initialize PiCamera
camera = PiCamera()

# Set camera resolution (adjust these values as needed)
camera.resolution = (640, 480)

# Start the camera
camera.start_preview()

# Create an OpenCV window
cv2.namedWindow("Text Detection", cv2.WINDOW_NORMAL)

# Initialize variables for frame skipping
frame_counter = 0
skip_frames = 5  # Process every 5th frame (adjust as needed)

try:
    while True:
        # Capture an image as a NumPy array
        frame = np.empty((camera.resolution[1] * camera.resolution[0] * 3,), dtype=np.uint8)
        camera.capture(frame, 'bgr')
        frame = frame.reshape((camera.resolution[1], camera.resolution[0], 3))

        if frame_counter % skip_frames == 0:
            d = pytesseract.image_to_data(frame, output_type=Output.DICT)
            n_boxes = len(d['text'])
            for i in range(n_boxes):
                if int(d['conf'][i]) > 60:
                    (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    if text and text.strip() != "":
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

            # Display the resulting frame
            cv2.imshow('Text Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        frame_counter += 1

finally:
    # Close the camera and destroy the OpenCV window
    camera.stop_preview()
    cv2.destroyAllWindows()
