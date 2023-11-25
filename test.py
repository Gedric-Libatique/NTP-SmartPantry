import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
import cv2
import pytesseract
from roboflow import Roboflow

# Initialize the Roboflow model
#rf = Roboflow(api_key="xkbIrK2MkTDbwkuRw4wW")
# project = rf.workspace().project("expiration-date-a4klq")
#project = rf.workspace().project("expiration-date-mexx5")
#model = project.version(4).model

# Set the desired prediction image dimensions 
prediction_image_width = 640
prediction_image_height = 640

# Data Init
dark = False
sortValue = -1
list = []
expireRange = 2
alertActive = False;
is_active = 0
clicked = 0

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
    return '⛔'
# Add to List
def addToList(tree, item):
    if alertActive == False:
        list.append(item)
        addEntry(tree, item)
        
def mouse_click(event, x, y, flags, param):
	global is_active
	if event == cv2.EVENT_LBUTTONDOWN:
		is_active = 1
		clicked = True

def mouse_click2(event, x, y, flags, param):
	global clicked
	if event == cv2.EVENT_LBUTTONDOWN:
		clicked = 1
		
# Begin scanning items
def startScanning():	
    global is_active, clicked
    img_counter = 0  # counter for image name
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

            img_name = "/home/team4pi/Documents/smartpantry/database/item{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            img = cv2.imread(img_name)
            cv2.imshow('Saved Image', img)
            cv2.namedWindow('Saved Image', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('Saved Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setMouseCallback('Saved Image', mouse_click2)
  
            while True:
                k = cv2.waitKey(1)
                if clicked == 1:
                    clicked = 0
                    break
  
            cv2.destroyWindow('Saved Image')
            img_counter += 1
            is_active = 0

    cap.release()
    cv2.destroyAllWindows()

# Add to Tree
def addEntry(tree, item):
    global alertActive
    tree.insert('', 'end', text="1", values=(str(item), dateCheck(item.date), str(item.date)))
    if dateCheck(item.date) == '⚠' or dateCheck(item.date) == '⛔':
        newAlert()
        alertActive = True
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
            if dateCheck(i.date) == '⚠' or dateCheck(i.date) == '⛔':
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
tableLegend = Label(window, text=('✅ = Safe to Distribute   ⚠ = Within ' + str(expireRange) + ' Days until Expiring   ⛔ = Past Expiration Date'), font=('Arial', 12), anchor=W, fg='black', bg='white', borderwidth=2)
tableLegend.pack(pady=15)

"""
# Search
entry = Entry(window, bd=2)
entry.pack()
search = Button(window, text=('Search for Item'), command=lambda:find(tree, entry.get()))
search.pack()
"""

# Scan Button
testCereal = Item('Test Cereal')
button = Button(window, text='Add Test Item (Replace with Scan Function)', width=50, command=lambda:startScanning())
button.pack(pady=15)

# Theme Button
colorButton = Button(window, text='Set to Dark Theme', width=16, fg='white', bg='gray30', highlightcolor='gray35',command=toggle)
colorButton.pack(anchor=SE, side=BOTTOM)

window.mainloop()
