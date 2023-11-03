import cv2
import numpy as np
import pytesseract

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame by frame
    ret, frame = cap.read()
    
    # Convert the image from BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Use Tesseract to find text in the image
    data = pytesseract.image_to_data(rgb, output_type=pytesseract.Output.DICT)
    
    # Iterate over each "word" that Tesseract found
    for i in range(len(data['text'])):
        # If the word is not an empty string, draw a rectangle around it
        if int(data['conf'][i]) > 60:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows when done
cap.release()
cv2.destroyAllWindows()
