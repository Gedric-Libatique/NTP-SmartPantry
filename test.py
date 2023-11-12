import cv2
import pytesseract
from roboflow import Roboflow

# Initialize the Roboflow model
rf = Roboflow(api_key="xkbIrK2MkTDbwkuRw4wW")
project = rf.workspace().project("expiration-date-a4klq")
model = project.version(3).model

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        print("Failed to grab frame")
        break

    # Assume the image is resized for prediction
    prediction_image_width = 640  # Example prediction dimensions
    prediction_image_height = 640
    frame_resized_for_prediction = cv2.resize(frame, (prediction_image_width, prediction_image_height))

    # Save the frame temporarily
    temp_img_path = "temp_frame.jpg"
    cv2.imwrite(temp_img_path, frame_resized_for_prediction)

    # Predict using Roboflow model
    prediction = model.predict(temp_img_path, confidence=50, overlap=30).json()

    # Scale factor for bounding box coordinates
    scale_x = frame.shape[1] / prediction_image_width
    scale_y = frame.shape[0] / prediction_image_height

    for obj in prediction['predictions']:
        x1 = int((obj['x'] - obj['width'] / 2) * scale_x)
        x2 = int((obj['x'] + obj['width'] / 2) * scale_x)
        y1 = int((obj['y'] - obj['height'] / 2) * scale_y)
        y2 = int((obj['y'] + obj['height'] / 2) * scale_y)
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # class_name = obj['class']
        # confidence = obj['confidence']
        # label = f"{class_name}: {confidence:.2f}"

        # # Calculate the position for the text (above the bounding box)
        # label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        # top = max(y1, label_size[1])
        # cv2.putText(frame, label, (x1, top - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Extract the region of interest (ROI) and use Tesseract to read the text
        roi = frame[y1:y2, x1:x2]
        # Use Tesseract to do OCR on the ROI
        text = pytesseract.image_to_string(roi, config='--psm 6')

        # Draw the bounding box and the OCR'd text above it
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Expiration Date Detection", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
