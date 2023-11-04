import tkinter as tk
from tkinter import filedialog
import cv2
import os
import threading

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

        while True:
            ret, frame = cap.read()
            cv2.imshow('Camera Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def display_images(self):
        image_dir = filedialog.askdirectory()
        image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

        for image in image_files:
            print(image)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
