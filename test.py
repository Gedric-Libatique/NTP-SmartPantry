import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Tk, Button, font
import cv2
import math
import pytesseract
from roboflow import Roboflow

# Initialize the Roboflow model
rf = Roboflow(api_key="xkbIrK2MkTDbwkuRw4wW")
# project = rf.workspace().project("expiration-date-a4klq") # Smaller model (200+ images)
# model = project.version(3).model
project = rf.workspace().project("expiration-date-mexx5") # Larger model (2000+ images)
model = project.version(4).model
accuracy = 35
over = 30

# Set the desired prediction image dimensions 
prediction_image_width = 640
prediction_image_height = 640
img_path = "/home/team4pi/Documents/smartpantry/database/"

# Data Init
dark = False
sortValue = -1
list = []
expireRange = 2
alertActive = False;
is_active = 0
clicked = 0
img_counter = 0

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
            if date.day - today.day < expireRange + 1 and date.day - today.day >= 0:
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
    global alertActive
    tree.insert('', 'end', text="1", values=(str(item), dateCheck(item.date), str(text)))
    '''
    if dateCheck(item.date) == '⚠' or dateCheck(item.date) == '×':
        newAlert()
        alertActive = True
    '''

# Add to List
def addToList(tree, item, text):
    if alertActive == False:
        list.append(item)
        addEntry(tree, item, text)

# Begin scanning items
def startScanning():	
    global is_active, clicked, img_counter
    prediction_image_width = 640
    prediction_image_height = 640
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

				# Use Tesseract to do OCR on the binary ROI
                text = pytesseract.image_to_string(roi, config='--psm 6')
                
                # Extract date and store in list
                print(text)
                scannedItem = Item("Pantry Item {}".format(img_counter))
                addToList(tree, scannedItem, text)

				# Draw the bounding box and the OCR'd text above it
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			# Find the contour with the largest area
            largest_contour = max(contours, key=cv2.contourArea)
            #largest_contour = max(contours, key=lambda contour: cv2.contourArea(contour))
            
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
                size = math.ceil(cv2.contourArea(contour))

                if contour == max_contour:
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

# Begin using live feed
def startLiveFeed():
	global is_active	
	cap = cv2.VideoCapture(0)
	prediction_image_width = 640
	prediction_image_height = 640
	
	while True:
		ret, frame = cap.read()
		if not ret:
			print("Failed to grab frame")
			break
			
		# Convert frame to grayscale
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame_resized_for_prediction = cv2.resize(frame_gray, (prediction_image_width, prediction_image_height))

		# Predict using Roboflow model 
		prediction = model.predict(frame_resized_for_prediction, confidence=accuracy, overlap=over).json()

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
			cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		# Display the frame
		cv2.namedWindow('Live Feed Detection', cv2.WINDOW_NORMAL)
		cv2.setWindowProperty('Live Feed Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		cv2.setMouseCallback('Live Feed Detection', mouse_click)
		cv2.imshow("Live Feed Detection", frame)

		# Exit the loop when the 'q' key is pressed
		k = cv2.waitKey(1)
		if k & 0xFF == ord('q'):
			break
		if is_active == 1:
			is_active = 0
			break

	# Release the capture when everything is done
	cap.release()
	cv2.destroyAllWindows()

# Alert Window
def newAlert():
    global alertActive
    if alertActive == False:
        
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
        alertActive = True
# Close
def die(b):
    b.destroy()
    global alertActive
    alertActive = False
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
boxTitle = Label(window, text='Item Inventory', font=('Arial', 24), fg='black', bg='white')
boxTitle.pack()

# Table Setup
treeFrame = Frame()
treeFrame.pack()
style = ttk.Style()
style.theme_use('clam')
tree = ttk.Treeview(treeFrame, column=('Item', 'Status', 'Expiration Date'), show='headings', height=10)

# Table Scrollbar
treeScroll = ttk.Scrollbar(treeFrame, orient='vertical', command=tree.yview)
treeScroll.pack(side='right', fill=Y)
tree.configure(yscrollcommand = treeScroll.set)

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
tableLegend = Label(window, text=('✅ = Safe to Distribute   ⚠ = Within ' + str(expireRange) + ' Days until Expiring   × = Past Expiration Date'), font=('Arial', 12), anchor=W, fg='black', bg='white', borderwidth=2)
tableLegend.pack(pady=15)

"""
# Search
entry = Entry(window, bd=2)
entry.pack()
search = Button(window, text=('Search for Item'), command=lambda:find(tree, entry.get()))
search.pack()
"""

# Scan Button
#testCereal = Item('Test Cereal')
custom_font = font.Font(family="Helvetica", size=25)
button = Button(window, text='Add Pantry Item', font=custom_font, width=50, height=2, bg="#00ff00", command=lambda:startScanning())
button.pack(pady=15)

# Live Scan Button
custom_font = font.Font(family="Helvetica", size=25)
button = Button(window, text='Live Feed', font=custom_font, width=50, height=2, bg="#ffff00", command=lambda:startLiveFeed())
button.pack(pady=15)

# Theme Button
colorButton = Button(window, text='Set to Dark Theme', width=16, fg='white', bg='gray30', highlightcolor='gray35',command=toggle)
colorButton.pack(anchor=SE, side=BOTTOM)

window.mainloop() # Testing done
