import tkinter as tk
from tkinter import filedialog
import cv2
import os
import threading
from pytesseract import pytesseract, Output  # Import pytesseract and Output
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.quit = tk.Button(self, text="Exit", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="top", anchor="ne")

        self.cam_button = tk.Button(self, text="Enable Camera", command=self.enable_camera)
        self.cam_button.pack(side="top")

        self.img_button = tk.Button(self, text="Display Images", command=self.display_images)
        self.img_button.pack(side="top")

    def enable_camera(self):
        cap = cv2.VideoCapture(0)
        img_counter = 0  # counter for image name
        
        while True:
        ret, frame = cap.read()
        cv2.imshow('Camera Feed', frame)
        
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):  # quit camera feed if 'q' is pressed
            break
        elif k & 0xFF == ord('p'):  # capture frame if 'p' is pressed
            img_name = "/home/team4pi/Documents/pantry/Dates/frame_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            
        cap.release()
        cv2.destroyAllWindows()

    def display_images(self):
        script_path = os.path.join(os.path.dirname(__file__), 'example.py')
        if os.path.exists(script_path):
            subprocess.Popen(['python', script_path])
        else:
            print("The script 'example.py' was not found in the same folder.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
