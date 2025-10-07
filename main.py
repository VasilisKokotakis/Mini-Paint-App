import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageGrab

# --------------------------
# Paint App Functions
# --------------------------

brush_color = "#222222"
brush_size = 5
last_x, last_y = None, None

def start_paint(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def paint(event):
    global last_x, last_y
    if last_x is not None and last_y is not None:
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=brush_color, width=brush_size * 2,
                           capstyle=tk.ROUND, smooth=True)
    last_x, last_y = event.x, event.y

def reset(event):
    global last_x, last_y
    last_x, last_y = None, None

def change_color(new_color):
    global brush_color
    brush_color = new_color
    update_status()

def change_size(new_size):
    global brush_size
    brush_size = new_size
    update_status()

def clear_canvas():
    canvas.delete("all")

def save_canvas():
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    img = ImageGrab.grab().crop((x, y, x1, y1))

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    if file_path:
        img.save(file_path)

def update_status():
    status_label.config(
        text=f"Color: {brush_color.upper()} | Size: {brush_size}"
    )
    brush_preview.config(bg=brush_color)

# --------------------------
# Main Window
# --------------------------

root = tk.Tk()
root.title("🎨 Modern Mini Paint")
root.geometry("800x500")
root.configure(bg="#f5f5f7")

style = ttk.Style()
style.theme_use("clam")

# Modern button style
style.configure("TButton",
                font=("Segoe UI", 10),
                padding=6,
                background="#ffffff",
                relief="flat")
style.map("TButton",
          background=[("active", "#e0e0e0")])

# Canvas
canvas = tk.Canvas(root, bg="white", highlightthickness=0, cursor="pencil")
canvas.pack(fill="both", expand=True, padx=10, pady=(10, 0))

# Bind events
canvas.bind("<Button-1>", start_paint)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", reset)

# Controls Frame
controls = ttk.Frame(root)
controls.pack(fill="x", pady=8)

# Colors
colors = ["#222222", "#e53935", "#1e88e5", "#43a047", "#fbc02d", "#8e24aa"]
for c in colors:
    b = tk.Button(controls, bg=c, width=2, height=1,
                  command=lambda col=c: change_color(col),
                  relief="flat", bd=0)
    b.pack(side="left", padx=4)

# Brush size buttons
for size, label in [(2, "Small"), (5, "Medium"), (10, "Large")]:
    ttk.Button(controls, text=label,
               command=lambda s=size: change_size(s)).pack(side="left", padx=4)

# Clear & Save buttons
ttk.Button(controls, text="🧹 Clear", command=clear_canvas).pack(side="left", padx=8)
ttk.Button(controls, text="💾 Save", command=save_canvas).pack(side="left", padx=4)

# Brush preview
brush_preview = tk.Label(controls, bg=brush_color, width=2, height=1, relief="flat")
brush_preview.pack(side="left", padx=12)

# Status Bar
status_label = tk.Label(root, text="", bg="#f5f5f7", fg="#555",
                        anchor="w", font=("Segoe UI", 9))
status_label.pack(fill="x", padx=10, pady=(0, 10))
update_status()

root.mainloop()
