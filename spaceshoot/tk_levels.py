import tkinter as tk
from PIL import Image,ImageTk
from level1 import gameloop

def on_click(event):
    canvas.itemconfig(circle,fill='gray')

def on_release(event):
    canvas.itemconfig(circle, fill='blue')
    gameloop()  # Start the game loop

def on_enter(event): # event for enter positon of mouse in button
    canvas.config(cursor='hand2')

def on_leave(event): # event for levening position of mouse out button 
    canvas.config(cursor='arrow')

# game variable 
width = 800
height = 700

# Create a window
root = tk.Tk()
root.title("Circular Button")
root.geometry(f"{width}x{height}")


# create a canvas 
canvas = tk.Canvas(root, width=width, height=height, bg="white", highlightthickness=5)
canvas.pack()

# load image 
image = Image.open('assests/bg.jpg')

# resize image
image = image.resize((width,height))

# convert image to tkinter image

tk_image = ImageTk.PhotoImage(image)

# Create a label to display the image

canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

# Create a circular shape (Oval)
circle = canvas.create_oval(width//2+50,height//2+50,width//2-50,height//2-50, fill="blue", outline="black")

# Add text in the center
text = canvas.create_text(width//2,height//2, text="Click Me", font=("Arial", 12, "bold"), fill="white")

# Bind pressing event to both circle and text
canvas.tag_bind(circle, "<Button-1>", on_click)
canvas.tag_bind(text, "<Button-1>", on_click)

# Bind releasing event to both circle and text 
canvas.tag_bind(circle,"<ButtonRelease-1>",on_release)
canvas.tag_bind(text,"<ButtonRelease-1>",on_release)


# bind circle event to mou position 
canvas.tag_bind(circle,"<Enter>",on_enter)
canvas.tag_bind(text,"<Enter>",on_enter)

# # on leveinng
canvas.tag_bind(circle,"<Leave>",on_leave)
canvas.tag_bind(text,"<Leave>",on_leave)

root.mainloop()