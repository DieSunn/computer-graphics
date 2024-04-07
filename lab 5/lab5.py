import tkinter as tk

def add_drawn_pixel(x, y):
    pixel_data = canvas.create_image(x, y, fill="black")
    drawn_pixels.append((x, y, pixel_data))

def is_same_color(pixel_color, target_color):
    return pixel_color == target_color

def flood_fill(start_x, start_y, target_color, fill_color):
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack.pop()

        if 0 <= x < canvas_width and 0 <= y < canvas_height:
            pixel_color = canvas.getpixel((x, y))

            if is_same_color(pixel_color, target_color):
                canvas.putpixel((x, y), fill_color)
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

def draw(event):
    global is_drawing
    if not is_fill_mode:
        is_drawing = True
        add_drawn_pixel(event.x, event.y)

def move(event):
    if is_drawing and not is_fill_mode:
        x, y = event.x, event.y
        add_drawn_pixel(x, y)

def release(event):
    global is_drawing
    is_drawing = False

def fill(event):
    global is_fill_mode
    if is_fill_mode:
        if not drawn_pixels:
            return

        x, y = event.x, event.y
        target_color = canvas.getpixel(drawn_pixels[0][:2])
        fill_color = (255, 255, 0)
        flood_fill(x, y, target_color, fill_color)

def set_draw_mode():
    global is_fill_mode
    is_fill_mode = False

def set_fill_mode():
    global is_fill_mode
    is_fill_mode = True

def clear_canvas():
    canvas.delete("all")
    drawn_pixels.clear()
    set_draw_mode()

root = tk.Tk()
root.title("Flood Fill Algorithm")

canvas_width = 400
canvas_height = 400

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

is_drawing = False
is_fill_mode = False
drawn_pixels = []

canvas.bind("<Button-1>", draw)
canvas.bind("<B1-Motion>", move)
canvas.bind("<ButtonRelease-1>", release)
canvas.bind("<Button-3>", fill)

draw_mode_button = tk.Button(root, text="Draw Mode", command=set_draw_mode)
draw_mode_button.pack(side=tk.LEFT)

fill_mode_button = tk.Button(root, text="Fill Mode", command=set_fill_mode)
fill_mode_button.pack(side=tk.LEFT)

clear_canvas_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_canvas_button.pack(side=tk.LEFT)

root.mainloop()
