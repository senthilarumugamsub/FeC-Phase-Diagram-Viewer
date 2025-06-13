# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 20:33:58 2025

@author: Senthil
"""
import tkinter as tk
from PIL import Image, ImageTk

# Constants
IMG_PATH = "Iron_carbon_phase_diagram.png"
IMG_WIDTH = 810
IMG_HEIGHT = 564

# Pixel bounds of actual axes
X_MIN_PX = 70
X_MAX_PX = 745
Y_MIN_PX = 46
Y_MAX_PX = 513

# Axis values
C_MIN, C_MAX = 0.0, 6.7
T_MIN, T_MAX = 25, 1600

img_tk = None  # Image reference
cursor_circle = None  # Will hold circle ID

def pixel_to_phase_coords(x, y):
    carbon = C_MIN + ((x - X_MIN_PX) / (X_MAX_PX - X_MIN_PX)) * (C_MAX - C_MIN)
    temperature = T_MAX - ((y - Y_MIN_PX) / (Y_MAX_PX - Y_MIN_PX)) * (T_MAX - T_MIN)
    return carbon, temperature

def on_mouse_move(event):
    global cursor_circle

    x, y = event.x, event.y

    if X_MIN_PX <= x <= X_MAX_PX and Y_MIN_PX <= y <= Y_MAX_PX:
        carbon, temp = pixel_to_phase_coords(x, y)
        coord_label.config(text=f"Carbon: {carbon:.2f} wt%   Temp: {temp:.1f} °C")

        # Update circle marker
        radius = 3
        if cursor_circle is not None:
            canvas.coords(cursor_circle, x - radius, y - radius, x + radius, y + radius)
        else:
            cursor_circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                               outline="red", fill="red")
    else:
        coord_label.config(text="")
        if cursor_circle:
            canvas.coords(cursor_circle, -10, -10, -10, -10)  # Move it offscreen

def main():
    global img_tk, coord_label, canvas

    root = tk.Tk()
    root.title("Fe-C Phase Diagram Viewer with Cursor Marker")

    img = Image.open(IMG_PATH)
    img_tk = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(root, width=IMG_WIDTH, height=IMG_HEIGHT)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=img_tk)

    coord_label = tk.Label(root, text="", font=("Arial", 14), fg="red")
    coord_label.pack(pady=5)

    canvas.bind("<Motion>", on_mouse_move)

    root.mainloop()

if __name__ == '__main__':
    main()
