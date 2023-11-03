import cv2
import pytesseract
from pytesseract import Output
import threading

# Create a lock to prevent simultaneous thread access to the frame
frame_lock = threading.Lock()

# Start video capture on a separate thread
def capture():
    global cap, frame
    while True:
        ret, f = cap.read()
        with frame_lock:
            frame = f

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Start the capture thread
cap_thread = threading.Thread(target=capture)
cap_thread.start()

frame_count = 0
while True:
    # Capture frame-by-frame
    with frame_lock:
        f = frame.copy()

    # Skip frames to improve FPS
    frame_count += 1
    if frame_count % 5 == 0:
        # Resize the frame
        f = cv2.resize(f, None, fx=0.5, fy=0.5)

        # Convert to grayscale
        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

        # Use Tesseract to find text in the image
        d = pytesseract.image_to_data(gray, output_type=Output.DICT)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # don't show empty text
                if text and text.strip() != "":
                    f = cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    f = cv2.putText(f, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        # Display the resulting frame
        cv2.imshow('frame', f)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
