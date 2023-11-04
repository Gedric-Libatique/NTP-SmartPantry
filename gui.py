import tkinter as tk
from tkinter import filedialog
import cv2
import os

# Function to show the live camera feed
def show_camera():
    camera = cv2.VideoCapture(0)
    
    def update_frame():
        ret, frame = camera.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = tk.PhotoImage(data=cv2image.tobytes())
            panel.img = img
            panel.config(image=img)
            panel.after(10, update_frame)
    
    camera_window = tk.Toplevel(root)
    camera_window.title("Camera Feed")
    panel = tk.Label(camera_window)
    panel.pack()
    update_frame()

# Function to list .jpg images in the current folder
def list_images():
    folder = os.getcwd()
    images = [file for file in os.listdir(folder) if file.endswith('.jpg')]
    
    image_list_window = tk.Toplevel(root)
    image_list_window.title("Image List")
    image_list = tk.Listbox(image_list_window)
    for image in images:
        image_list.insert(tk.END, image)
    image_list.pack()

# Create the main window
root = tk.Tk()
root.title("Simple UI")

# Create buttons
camera_button = tk.Button(root, text="Live Camera Feed", command=show_camera)
image_list_button = tk.Button(root, text="List .jpg Images", command=list_images)
exit_button = tk.Button(root, text="Exit", command=root.destroy)

# Pack the buttons
camera_button.pack()
image_list_button.pack()
exit_button.pack()

# Start the GUI main loop
root.mainloop()
