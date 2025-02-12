import tkinter as tk
from tkinter import messagebox

def on_space(event):
    messagebox.showinfo("Message Box", "Space bar was pressed")

root = tk.Tk()
root.title("Simple Tkinter Window")
root.geometry("300x200")

label = tk.Label(root, text="Press the space bar")
label.pack(pady=50)

root.bind('<space>', on_space)

root.mainloop()
