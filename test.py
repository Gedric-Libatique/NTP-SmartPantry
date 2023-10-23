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
            frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
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
