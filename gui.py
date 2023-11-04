import tkinter as tk
from tkinter import filedialog
import cv2
import os
import threading
from pytesseract import pytesseract, Output  # Import pytesseract and Output

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
            d = pytesseract.image_to_data(frame, output_type=Output.DICT)
            n_boxes = len(d['text'])

            for i in range(n_boxes):
                if int(d['conf'][i]) > 60:
                    (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    # don't show empty text
                    if text and text.strip() != "":
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

            # Display the resulting frame
            cv2.imshow('frame', frame)

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
