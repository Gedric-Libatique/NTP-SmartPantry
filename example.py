import cv2
import pytesseract
import numpy as np
import os
from pytesseract import Output

# Define the folder containing the images
image_folder = 'Dates'  # Update this to the path of your image folder

# Get a list of image files in the folder
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def morph_opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def canny(image):
    return cv2.Canny(image, 100, 200)

for image_file in image_files:
    img_source = cv2.imread(image_file)
    
    gray = get_grayscale(img_source)
    thresh = thresholding(gray)
    opened = morph_opening(gray)  # Changed variable name to 'opened'
    canny_img = canny(gray)  # Changed variable name to 'canny_img'

    for img in [img_source, gray, thresh, opened, canny_img]:  # Updated variable names here
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['text'])

        # Convert grayscale images back to RGB
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # Don't show empty text
                if text and text.strip() != "":
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    img = cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        cv2.imshow('img', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()
