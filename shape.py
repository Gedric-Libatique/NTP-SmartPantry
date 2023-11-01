import cv2
import time

cap = cv2.VideoCapture(0)  # Use the default camera (change the index if you have multiple cameras)
while True:
    ret, frame = cap.read()  # Capture a frame

    # Preprocessing steps go here (e.g., convert to grayscale, blur, adjust contrast)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to create a binary image
    _, thresholded = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process detected contours
    for contour in contours:
        # Approximate the contour to simplify shape detection
        x, y, w, h = cv2.boundingRect(contour)
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Identify the shape based on the number of vertices
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            shape = "Rectangle"
        else:
            shape = "Circle"

        # Calculate the size (area) of the object
        size = cv2.contourArea(contour)

        # Draw the detected object on the frame
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        cv2.putText(frame, f"{shape} ({size:.2f})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the frame with object detection
    cv2.imshow("Object Detection", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
