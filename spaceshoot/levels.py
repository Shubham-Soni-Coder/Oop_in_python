import tkinter as tk

def on_click(event):
    canvas.itemconfig(circle,fill='gray')

def on_relase(event):
    canvas.itemconfig(circle,fill='blue')
    print('Hello User')
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

canvas = tk.Canvas(root, width=width, height=height, bg="white", highlightthickness=0)
canvas.pack()

# Create a circular shape (Oval)
circle = canvas.create_oval(width//2+100,height//2+100,width//2-100,height//2-100, fill="blue", outline="black")

# Add text in the center
text = canvas.create_text(width//2,height//2, text="Click Me", font=("Arial", 12, "bold"), fill="white")

# Bind pressing event to both circle and text
canvas.tag_bind(circle, "<Button-1>", on_click)
canvas.tag_bind(text, "<Button-1>", on_click)

# Bind relaseing event to both circle and text 
canvas.tag_bind(circle,"<ButtonRelease-1>",on_relase)
canvas.tag_bind(circle,"<ButtonRelease-1>",on_relase)


# bind circle event to mou position 
canvas.tag_bind(circle,"<Enter>",on_enter)
canvas.tag_bind(text,"<Enter>",on_enter)

# # on leveinng
canvas.tag_bind(circle,"<Leave>",on_leave)
canvas.tag_bind(text,"<Leave>",on_leave)

root.mainloop()
