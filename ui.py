import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Data Init
dark = False
sortValue = -1
list = []
expireRange = 2

# Functions
class Item:
    def __init__(self, name, date = datetime.date.today()):
        self.name = name
        self.date = date
    def __str__(self):
        return f'{self.name}'
    def __eq__(self, other):
        return self.name == other.name
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
def addToList(tree, item):
    list.append(item)
    addEntry(tree, item)
def addEntry(tree, item):
    tree.insert('', 'end', text="1", values=(str(item), dateCheck(item.date), str(item.date)))
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
# Test cases
list.append(Item('Soup'))
list.append(Item('Clam Chowder'))
list.append(Item('Tuna Snack'))
list.append(Item('Oatmeal', datetime.date(2023, 11, 8)))
list.append(Item('Oatmeal', datetime.date(2023, 11, 9)))
list.append(Item('Oatmeal', datetime.date(2020, 9, 10)))
list.append(Item('Oatmeal', datetime.date(2020, 12, 20)))
list.append(Item('Tuna Snack', datetime.date(2023, 10, 10)))
list.append(Item('Corned Beef', datetime.date(2023, 11, 6)))
list.append(Item('Crisp Rice Cereal', datetime.date(2023, 11, 12)))
list.append(Item('Crackers', datetime.date(2023, 12, 20)))
list.append(Item('Tomato Paste', datetime.date(2024, 10, 10)))
list.append(Item('Tomato Paste', datetime.date(2024, 6, 2)))

# Window
window = Tk()
# window.attributes('-fullscreen',True)
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
tableLegend.pack()

# Scan Button
testCereal = Item('Test Cereal')
button = Button(window, text='Add Test Item (Replace with Scan Function)', width=50, command=lambda:addToList(tree, testCereal))
button.pack()

# Theme Button
colorButton = Button(window, text='Set to Dark Theme', width=16, fg='white', bg='gray30', highlightcolor='gray35',command=toggle)
colorButton.pack(anchor=SE, side=BOTTOM)

window.mainloop()