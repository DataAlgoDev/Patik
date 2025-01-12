import tkinter as tk
from tkinter import messagebox

def on_closing():
    # Ask the user if they really want to quit
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()  # Close the window

root = tk.Tk()
root.title("Exit Confirmation Example")

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Add a simple label to the window
label = tk.Label(root, text="Click the X to exit.")
label.pack(padx=20, pady=20)

root.mainloop()
