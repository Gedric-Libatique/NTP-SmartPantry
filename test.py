import tkinter as tk

# Run using: python3 test.py
# Run to install tkinter on Pi: sudo apt-get install python3-tk

def display_text():
    # Create a new tkinter window
    window = tk.Tk()

    # Set the window title
    window.title("Raspberry Pi Display")

    # Create a label with your text
    label = tk.Label(window, text="Hello, Raspberry Pi 4!")

    # Add the label to the window
    label.pack()

    # Run the tkinter event loop
    window.mainloop()

# Call the function to display the text
display_text()