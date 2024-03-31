import tkinter as tk
from math import pi, radians, cos, sin

def draw_ellipse():
    width = int(width_entry.get())
    height = int(height_entry.get())
    
    canvas.delete("all")
    
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2
    
    draw_quarter_ellipse(center_x, center_y, width / 2, height / 2, 0, pi / 2)
    draw_quarter_ellipse(center_x, center_y, width / 2, height / 2, pi / 2, pi)
    draw_quarter_ellipse(center_x, center_y, width / 2, height / 2, pi, pi * 1.5)
    draw_quarter_ellipse(center_x, center_y, width / 2, height / 2, pi * 1.5, pi * 2)

def draw_quarter_ellipse(center_x, center_y, width, height, start_angle, end_angle):
    num_segments = 100
    angle_delta = (end_angle - start_angle) / num_segments
    
    points = []
    for i in range(num_segments + 1):
        angle = start_angle + i * angle_delta
        x = center_x + width * cos(angle)
        y = center_y + height * sin(angle)
        points.append((x, y))
    
    for i in range(num_segments):
        canvas.create_line(points[i], points[i+1])

def rotate_ellipse():
    angle = int(angle_entry.get())
    canvas.delete("all")
    
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill="white")
    
    canvas.create_text(canvas.winfo_width() / 2, 20, text="Rotated Ellipse", font=("Helvetica", 16))
    
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2
    
    canvas.create_text(center_x, center_y, text="Original Ellipse", font=("Helvetica", 12))
    
    canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="gray")
    canvas.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="gray")
    
    draw_ellipse()
    
    canvas.after(100, lambda: rotate_ellipse_animation(center_x, center_y, angle))

def rotate_ellipse_animation(center_x, center_y, angle):
    canvas.delete("all")
    
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill="white")
    
    rotated_center_x = canvas.winfo_width() / 2
    rotated_center_y = canvas.winfo_height() / 2

    canvas.create_line(rotated_center_x - 50, rotated_center_y, rotated_center_x + 50, rotated_center_y, fill="gray")
    canvas.create_line(rotated_center_x, rotated_center_y - 50, rotated_center_x, rotated_center_y + 50, fill="gray")
    
    canvas.create_text(rotated_center_x, rotated_center_y, text=f"Rotated by {angle} degrees", font=("Helvetica", 12))
    
    canvas.create_line(rotated_center_x - 50, rotated_center_y, rotated_center_x + 50, rotated_center_y, fill="gray")
    canvas.create_line(rotated_center_x, rotated_center_y - 50, rotated_center_x, rotated_center_y + 50, fill="gray")
    
    draw_ellipse_rotated(rotated_center_x, rotated_center_y, int(width_entry.get()) / 2, int(height_entry.get()) / 2, radians(angle))
    

def draw_ellipse_rotated(center_x, center_y, width, height, angle):
    num_segments = 100
    angle_delta = 2 * pi / num_segments
    
    points = []
    for i in range(num_segments + 1):
        current_angle = i * angle_delta
        rotated_x = center_x + (width * cos(current_angle) * cos(angle) - height * sin(current_angle) * sin(angle))
        rotated_y = center_y + (width * cos(current_angle) * sin(angle) + height * sin(current_angle) * cos(angle))
        points.append((rotated_x, rotated_y))
    
    for i in range(num_segments):
        canvas.create_line(points[i], points[i+1])

# GUI Setup
root = tk.Tk()
root.title("Ellipses")
root.geometry("600x400")

canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(side=tk.LEFT, padx=20, pady=20)

control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, padx=20)

width_label = tk.Label(control_frame, text="Width:")
width_label.grid(row=0, column=0, padx=5, pady=5)

width_entry = tk.Entry(control_frame)
width_entry.grid(row=0, column=1, padx=5, pady=5)

height_label = tk.Label(control_frame, text="Height:")
height_label.grid(row=1, column=0, padx=5, pady=5)

height_entry = tk.Entry(control_frame)
height_entry.grid(row=1, column=1, padx=5, pady=5)

draw_button = tk.Button(control_frame, text="Draw Ellipse", command=draw_ellipse)
draw_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

angle_label = tk.Label(control_frame, text="Rotation Angle:")
angle_label.grid(row=3, column=0, padx=5, pady=5)

angle_entry = tk.Entry(control_frame)
angle_entry.grid(row=3, column=1, padx=5, pady=5)

rotate_button = tk.Button(control_frame, text="Rotate Ellipse", command=rotate_ellipse)
rotate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
