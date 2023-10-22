import cv2
import pytesseract

cap = cv2.VideoCapture(0)  # Use the default camera (change the index if you have multiple cameras)

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

# import tkinter as tk

# # Run using: python3 test.py
# # Run to install tkinter on Pi: sudo apt-get install python3-tk

# def display_text():
#     # Create a new tkinter window
#     window = tk.Tk()

#     # Set the window title
#     window.title("Raspberry Pi Display")

#     # Create a label with your text
#     label = tk.Label(window, text="Hello, Raspberry Pi 4!")

#     # Add the label to the window
#     label.pack()

#     # Run the tkinter event loop
#     window.mainloop()

# # Call the function to display the text
# display_text()