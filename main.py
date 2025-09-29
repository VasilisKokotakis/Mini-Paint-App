import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab  # for saving drawings

# --------------------------
# Paint App Functions
# --------------------------

brush_color = "black"
brush_size = 5
last_x, last_y = None, None  # store previous mouse position

def start_paint(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def paint(event):
    global last_x, last_y
    if last_x is not None and last_y is not None:
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=brush_color, width=brush_size*2,
                           capstyle=tk.ROUND, smooth=True)
    last_x, last_y = event.x, event.y

def reset(event):
    global last_x, last_y
    last_x, last_y = None, None

def change_color(new_color):
    global brush_color
    brush_color = new_color

def change_size(new_size):
    global brush_size
    brush_size = new_size

def clear_canvas():
    canvas.delete("all")

def save_canvas():
    # Get coordinates of canvas
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    # Grab canvas as image
    img = ImageGrab.grab().crop((x, y, x1, y1))

    # Save dialog
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if file_path:
        img.save(file_path)

# --------------------------
# Main Window
# --------------------------

root = tk.Tk()
root.title("Mini Paint App")

# Canvas
canvas = tk.Canvas(root, bg="white", width=600, height=400)
canvas.pack(fill="both", expand=True)

# Bind mouse events for smooth drawing
canvas.bind("<Button-1>", start_paint)       # mouse press
canvas.bind("<B1-Motion>", paint)            # mouse drag
canvas.bind("<ButtonRelease-1>", reset)      # mouse release

# Controls Frame
controls = tk.Frame(root)
controls.pack()

# Color buttons
colors = ["black", "red", "blue", "green", "yellow", "purple"]
for c in colors:
    tk.Button(controls, text=c.capitalize(),
              command=lambda col=c: change_color(col)).pack(side="left")

# Brush size buttons
tk.Button(controls, text="Small", command=lambda: change_size(2)).pack(side="left")
tk.Button(controls, text="Medium", command=lambda: change_size(5)).pack(side="left")
tk.Button(controls, text="Large", command=lambda: change_size(10)).pack(side="left")

# Clear & Save buttons
tk.Button(controls, text="Clear", command=clear_canvas).pack(side="left")
tk.Button(controls, text="Save", command=save_canvas).pack(side="left")

root.mainloop()
