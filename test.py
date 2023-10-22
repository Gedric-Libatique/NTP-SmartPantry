import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import cv2
import pytesseract
import numpy as np

# Initialize GStreamer
Gst.init(None)

# Create a GStreamer pipeline for video capture
pipeline = Gst.parse_launch("v4l2src ! videoconvert ! video/x-raw,format=BGR ! appsink")

# Set up a callback function to process each frame
def on_new_sample(appsink):
    sample = appsink.emit("pull-sample")
    buffer = sample.get_buffer()
    
    if buffer:
        success, frame = buffer.extract_dup(0, buffer.get_size())
        
        if success:
            # Use Tesseract to perform OCR on the frame
            frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            detected_text = pytesseract.image_to_string(frame)

            # Display the detected text on the frame
            cv2.putText(frame, detected_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the frame with detected text
            cv2.imshow("Text Detection", frame)
    
    return Gst.FlowReturn.OK

# Configure the appsink element to call the callback function
appsink = pipeline.get_by_name("appsink0")
appsink.set_property("emit-signals", True)
appsink.connect("new-sample", on_new_sample)

# Start the GStreamer pipeline
pipeline.set_state(Gst.State.PLAYING)

# Main loop
try:
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    pass
finally:
    # Stop the GStreamer pipeline
    pipeline.set_state(Gst.State.NULL)
    cv2.destroyAllWindows()
