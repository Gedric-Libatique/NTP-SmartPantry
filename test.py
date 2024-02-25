import os, cv2, json, math, requests, datetime, pytesseract
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Tk, Button, font
from roboflow import Roboflow
from pyzbar.pyzbar import decode
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Initialize Azure OCR API
os.environ["VISION_KEY"] = "4eeff2b7a10542bba2755eac69a2b046"
os.environ["VISION_ENDPOINT"] = "https://seniordesignocr.cognitiveservices.azure.com/"

# Initialize Roboflow API 
rf = Roboflow(api_key="LkV23QCGFQJqWru2RYvL")

# Initialize large model (2000+ images)
project = rf.workspace().project("expiration-date-mexx5")
model = project.version(4).model

# Initialize small model (200+ images)
# project = rf.workspace().project("expiration-date-a4klq")
# model = project.version(3).model

# Set the desired prediction image dimensions 
prediction_image_width = 640
prediction_image_height = 640

# Initialize global variables
accuracy = 35
over = 30
dark = False
sortValue = -1
list = []
expire_range = 2
alert_active = False;
is_active = 0
clicked = 0
img_counter = 0
current_date = ""
current_name = ""
ocr_scale = 5

# Functions
class Item:
    def __init__(self, name, date = datetime.date.today()):
        self.name = name
        self.date = date
    def __str__(self):
        return f'{self.name}'
    def __eq__(self, other):
        return self.name == other.name

# Check Dates
def dateCheck(date):
    today = datetime.date.today()
    if date.year > today.year:
        return '✅'
    elif date.year == today.year:    
        if date.month > today.month:
            return '✅'
        elif date.month == today.month:
            if date.day - today.day < expire_range + 1 and date.day - today.day >= 0:
                return '⚠'
            elif date.day > today.day:
                return '✅'
    return '×'
        
def mouse_click(event, x, y, flags, param):
	global is_active
	if event == cv2.EVENT_LBUTTONDOWN:
		is_active = 1
		clicked = True

def mouse_click2(event, x, y, flags, param):
	global clicked
	if event == cv2.EVENT_LBUTTONDOWN:
		clicked = 1

# Add to Tree
def addEntry(tree, item, text):
    global alert_active
    tree.insert('', 'end', text="1", values=(str(item), dateCheck(item.date), str(text)))
    '''
    if dateCheck(item.date) == '⚠' or dateCheck(item.date) == '×':
        newAlert()
        alert_active = True
    '''

# Add to List
def addToList(tree, item, text):
    if alert_active == False:
        list.append(item)
        addEntry(tree, item, text)
        
# Read barcode for item identification
def getProductName(barcode):
    # Initialize barcode reader API
    api_key = '95vlr1c0rjim6gkqvyujz7v6kkdh8i'

    url = f"https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key=95vlr1c0rjim6gkqvyujz7v6kkdh8i"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Assuming the JSON response structure includes a 'products' list
        if data['products']:
            product_name = data['products'][0]['title']
            return product_name
        else:
            return "Product not found."
    else:
        return f"Error: {response.status_code}"

# Scan for barcode on product
def scanBarcode():
    global current_name
    cap = cv2.VideoCapture(0)
    camera = True

    while camera:
        success, frame = cap.read()
        cv2.namedWindow('Testing-code-scan', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Testing-code-scan', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        for code in decode(frame):
            barcode_data = code.data.decode('utf-8')
            print("Scanned barcode:", barcode_data)
            product_name = getProductName(barcode_data)
            current_name = product_name
            print("Product name:", product_name)
            # You may want to break after the first successful read and product name retrieval
            camera = False  # This will exit the while loop after one successful scan
            break  # Break the for loop after finding a barcode

        cv2.imshow('Testing-code-scan', frame)
        if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit the camera scan
            break

    cap.release()
    cv2.destroyAllWindows()

# Read scanned date using Azure AI
def readDateText(myPath):
    global current_date

    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()

    # Create an Image Analysis client
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Load image to analyze into a 'bytes' object
    with open(myPath, "rb") as f:
        image_data = f.read()

    # Extract text (OCR) from an image stream. This will be a synchronously (blocking) call.
    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

    # Print text (OCR) analysis results to the console
    print("Image analysis results:")
    print(" Read:")
    if result.read is not None:
        for line in result.read.blocks[0].lines:
            print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
            for word in line.words:
                print(f"     Word: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.4f}")
    print(f" Image height: {result.metadata.height}")
    print(f" Image width: {result.metadata.width}")
    print(f" Model version: {result.model_version}")
    current_date = line.text

# Begin scanning items
def startScanning():
    scanBarcode() # Scan barcode first
    global is_active, clicked, img_counter, current_date, current_name, prediction_image_width, prediction_image_height, ocr_scale
    cap = cv2.VideoCapture(0)
   
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Camera Feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback('Camera Feed', mouse_click)
        cv2.imshow('Camera Feed', frame)
		
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):  # quit camera feed if 'q' is pressed
            break
        if is_active == 1:
            cv2.destroyWindow('Camera Feed')
            print("Proceeding to capture....")
            
            # Set preview properties to full screen
            cv2.namedWindow('Saved Image', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('Saved Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setMouseCallback('Saved Image', mouse_click2)
            
            # Save captured frame to database
            img_name = "/home/team4pi/Documents/smartpantry/database/item{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            img = cv2.imread(img_name)
            
            # Convert frame to grayscale
            frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            frame_resized_for_prediction = cv2.resize(frame_gray, (prediction_image_width, prediction_image_height))
            
            # Apply thresholding to create a binary image
            _, thresholded = cv2.threshold(frame_gray, 128, 255, cv2.THRESH_BINARY)
            # Find contours in the binary image
            contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Predict using Roboflow model 
            prediction = model.predict(frame_resized_for_prediction, confidence=accuracy, overlap=over).json()
            
            # Scale factors 
            scale_x = img.shape[1] / prediction_image_width
            scale_y = img.shape[0] / prediction_image_height
			
			# Process predictions and draw bounding boxes and text
            for obj in prediction['predictions']:
                x1 = int((obj['x'] - obj['width'] / 2) * scale_x)
                x2 = int((obj['x'] + obj['width'] / 2) * scale_x)
                y1 = int((obj['y'] - obj['height'] / 2) * scale_y)
                y2 = int((obj['y'] + obj['height'] / 2) * scale_y)
				
				# Define the region of interest (ROI) based on the bounding box
                roi = img[y1:y2, x1:x2]
                
                # Resize the ROI back to the original resolution
                roi_resized = cv2.resize(roi, (ocr_scale*(x2 - x1), ocr_scale*(y2 - y1)))

				# Save the ROI to a file
                cropped_img = "/home/team4pi/Documents/smartpantry/database/item{}_cropped.jpg".format(img_counter)
                cv2.imwrite(cropped_img, roi_resized)
                readDateText(cropped_img)
               
                # Extract date and store in list
                text = current_date
                print(text)
                scannedItem = Item(current_name)
                addToList(tree, scannedItem, text)

				# Draw the bounding box and the OCR'd text above it
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			# Find the contour with the largest area
            largest_contour = max(contours, key=lambda contour: cv2.contourArea(contour))
            
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

                if cv2.contourArea(contour) == cv2.contourArea(largest_contour):
					# Calculate the size (area) of the object 
                    size = math.ceil(cv2.contourArea(contour))
					
                    # Draw the detected object on the frame
                    cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
                    cv2.putText(img, f"{shape} ({size:.2f})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Display the frame
            cv2.imshow('Saved Image', img)
              
            while True:
                k = cv2.waitKey(1)
                if clicked == 1:
                    clicked = 0
                    break
  
            cv2.destroyWindow('Saved Image')
            img_counter += 1
            is_active = 0
            break

    cap.release()
    cv2.destroyAllWindows()

# Alert Window
def newAlert():
    global alert_active
    if alert_active == False:
        
        alertWindow = Toplevel(window)
        alertWindow.attributes('-topmost', True)
        alertWindow.overrideredirect(True)
        alertWindow.geometry('+%d+%d'%(window.winfo_screenmmwidth() / 2, window.winfo_screenmmheight() / 2))
        
        Label(alertWindow, text=('Warning!\nThe following items are close to or are expired!'), font=('Arial', 12), anchor=N, fg='black', bg='white', borderwidth=2).pack() 
        # Table Setup
        alertTreeFrame = Frame(alertWindow)
        alertTreeFrame.pack()
        style = ttk.Style()
        style.theme_use('clam')
        alertTree = ttk.Treeview(alertTreeFrame, column=('Item', 'Expiration Date'), show='headings', height=5)

        # Table Scrollbar
        alertTreeScroll = ttk.Scrollbar(alertTreeFrame, orient='vertical', command=alertTree.yview)
        alertTreeScroll.pack(side='right', fill=Y)
        alertTree.configure(yscrollcommand = alertTreeScroll.set)

        # Table Entries
        alertTree.column('# 1', anchor=CENTER)
        alertTree.heading('# 1', text='Item', command=lambda:sortA(alertTree))
        alertTree.column('# 2', anchor=CENTER)
        alertTree.heading('# 2', text='Date', command=lambda:sortE(alertTree))
        for i in list:
            if dateCheck(i.date) == '⚠' or dateCheck(i.date) == '×':
                alertTree.insert('', 'end', text="1", values=(str(i), str(i.date)))
        alertTree.pack()
        
        alertButton = Button(alertWindow, text='Close', width=50, command=lambda:die(alertWindow))
        alertButton.pack()
        alert_active = True

# Close
def die(b):
    b.destroy()
    global alert_active
    alert_active = False
# Toggle Modes
def toggle():
    global dark
    if dark:
        window.configure(background='white')
        boxTitle.configure(fg='black', bg='white')
        tableLegend.configure(fg='black', bg='white')
        colorButton.configure(text='Set to Dark Theme')
        dark = False
    else:
        window.configure(background='black')
        boxTitle.configure(fg='white', bg='black')
        tableLegend.configure(fg='white', bg='black')
        colorButton.configure(text='Set to Light Theme')
        dark = True
# Sort Alphabetically
def sortA(tree):
    global sortValue
    if sortValue == 1:
        rows = [(tree.set(item, 'Item').lower(), item) for item in tree.get_children('')]
        rows.sort(reverse=True)
        for index, (values, item) in enumerate(rows):
            tree.move(item, '', index)
        sortValue = 2
    elif sortValue == 2:
        rows = [(tree.set(item, 'Item').lower(), item) for item in tree.get_children('')]
        rows.sort()
        for index, (values, item) in enumerate(rows):
            tree.move(item, '', index)
        sortValue = 1
    else:
        rows = [(tree.set(item, 'Item').lower(), item) for item in tree.get_children('')]
        rows.sort()
        for index, (values, item) in enumerate(rows):
            tree.move(item, '', index)
        sortValue = 1
# Sort by Date
def sortE(tree):
    global sortValue
    if sortValue == 3:
        rows = [(tree.set(item, 'Expiration Date').lower(), item) for item in tree.get_children('')]
        rows.sort(reverse=True)
        for index, (values, item) in enumerate(rows):
            tree.move(item, '', index)
        sortValue = 4
    elif sortValue == 4:
        rows = [(tree.set(item, 'Expiration Date').lower(), item) for item in tree.get_children('')]
        rows.sort()
        for index, (values, item) in enumerate(rows):
            tree.move(item, '', index)
        sortValue = 3
    else:
        rows = [(tree.set(item, 'Expiration Date').lower(), item) for item in tree.get_children('')]
        rows.sort()
        for index, (values, item) in enumerate(rows):
            tree.move(item, '', index)
        sortValue = 3
"""
# Find in Tree
def find(t, searchItem):
    for i in t.get_children():
        if t.item(i)['values'][0].lower().__contains__(str(searchItem).lower()):
            tid = i
            t.focus(tid)
            t.selection_set(tid)
            t.see(i)
            break
"""
# Window
window = Tk()
window.attributes('-fullscreen',True)
window.attributes('-topmost', False)
window.title('Smart Pantry')
icon = PhotoImage(file='./icon.ppm')
window.iconphoto(False, icon)
window.configure(background='white', padx=10, pady=10)

# Logo
canvas = Canvas(window, width=106, height=117)
canvas.pack(anchor=NW)
img = PhotoImage(file='./logosmall.ppm')
canvas.create_image(0,0, anchor=NW, image=img)

# Table Title
current_time = datetime.date.today().strftime('%m/%d/%y')
boxTitle = Label(window, text=f"Item Inventory ({current_time})", font=('Arial', 32), fg='black', bg='white')
boxTitle.pack()

# Table Setup
treeFrame = Frame()
treeFrame.pack()
style = ttk.Style()
style.theme_use('clam')
table_entries_font = font.Font(family="Helvetica", size=13)
style.configure('Treeview', font=table_entries_font)
tree = ttk.Treeview(treeFrame, column=('Item', 'Status', 'Expiration Date'), show='headings', height=10)

# Table Scrollbar
treeScroll = ttk.Scrollbar(treeFrame, orient='vertical', command=tree.yview)
treeScroll.pack(side='right', fill=Y)
tree.configure(yscrollcommand = treeScroll.set)

# Set column widths
tree.column('Item', width=400, minwidth=400, anchor=CENTER)
tree.column('Status', width=80, minwidth=80, anchor=CENTER)
tree.column('Expiration Date', width=150, minwidth=150, anchor=CENTER)

# Table Entries
tree.column('# 1', anchor=CENTER)
tree.heading('# 1', text='Item', command=lambda:sortA(tree))
tree.column('# 2', anchor=CENTER)
tree.heading('# 2', text='Status', command=lambda:sortE(tree))
tree.column('# 3', anchor=CENTER)
tree.heading('# 3', text='Expiration Date', command=lambda:sortE(tree))
for i in list:
    addEntry(tree, i)
tree.pack()

# Table Legend
tableLegend = Label(window, text=('✅ = Safe to Distribute   ⚠ = Within ' + str(expire_range) + ' Days until Expiring   × = Past Expiration Date'), font=('Arial', 12), anchor=W, fg='black', bg='white', borderwidth=2)
tableLegend.pack(pady=15)

"""
# Search
entry = Entry(window, bd=2)
entry.pack()
search = Button(window, text=('Search for Item'), command=lambda:find(tree, entry.get()))
search.pack()
"""

# Scan Button
scan_button_font = font.Font(family="Helvetica", size=35)
button = Button(window, text='Add Pantry Item', font=scan_button_font, width=40, height=2, bg="#00ff00", command=lambda:startScanning())
button.pack(pady=50)

# Theme Button
colorButton = Button(window, text='Set to Dark Theme', width=16, fg='white', bg='gray30', highlightcolor='gray35',command=toggle)
colorButton.pack(anchor=SE, side=BOTTOM)

window.mainloop()
