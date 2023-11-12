import cv2
import pytesseract
from roboflow import Roboflow

# Initialize the Roboflow model
rf = Roboflow(api_key="xkbIrK2MkTDbwkuRw4wW")
project = rf.workspace().project("expiration-date-a4klq")
model = project.version(3).model

# Start video capture
cap = cv2.VideoCapture(0)

# Set the desired prediction image dimensions 
prediction_image_width = 640
prediction_image_height = 640

while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        print("Failed to grab frame")
        break

    frame_resized_for_prediction = cv2.resize(frame, (prediction_image_width, prediction_image_height))

    # Predict using Roboflow model 
    prediction = model.predict(frame_resized_for_prediction, confidence=30, overlap=30).json()

    # Scale factors 
    scale_x = frame.shape[1] / prediction_image_width
    scale_y = frame.shape[0] / prediction_image_height

    # Process predictions and draw bounding boxes and text
    for obj in prediction['predictions']:
        
        x1 = int((obj['x'] - obj['width'] / 2) * scale_x)
        x2 = int((obj['x'] + obj['width'] / 2) * scale_x)
        y1 = int((obj['y'] - obj['height'] / 2) * scale_y)
        y2 = int((obj['y'] + obj['height'] / 2) * scale_y)
        
        # Define the region of interest (ROI) based on the bounding box
        roi = frame[y1:y2, x1:x2]

        # Use Tesseract to do OCR on the binary ROI
        text = pytesseract.image_to_string(roi, config='--psm 6')

        # Draw the bounding box and the OCR'd text above it
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Expiration Date Detection", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()
