import cv2
import pytesseract
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Create a GStreamer pipeline to capture video from the default camera
pipeline = Gst.parse_launch("v4l2src ! videoconvert ! appsink")

# Create an OpenCV VideoCapture object with the pipeline
cap = cv2.VideoCapture(pipeline.get_property('name'), cv2.CAP_GSTREAMER)

while True:
    ret, frame = cap.read()  # Capture a frame

    # Use Tesseract to perform OCR on the frame
    detected_text = pytesseract.image_to_string(frame)

    # Display the detected text on the frame
    cv2.putText(frame, detected_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with detected text
    cv2.imshow("Text Detection", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
