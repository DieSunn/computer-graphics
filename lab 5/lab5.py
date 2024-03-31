import tkinter as tk
from tkinter import messagebox

# Создание окна
root = tk.Tk()
root.title("Canvas Drawing and Flood Fill")

# Создание холста
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Переменные состояния
is_drawing = False
is_fill_mode = False

# Список для хранения нарисованных линий и пикселей
drawn_elements = []

# Функция для рисования линии
def draw_line(start_x, start_y, end_x, end_y):
    line = canvas.create_line(start_x, start_y, end_x, end_y, fill="black", width=3)
    drawn_elements.append(line)

# Функция для добавления нарисованного пикселя
def add_drawn_pixel(x, y):
    pixel = canvas.create_rectangle(x, y, x+1, y+1, fill="black")
    drawn_elements.append(pixel)

# Функция для проверки, является ли цвет однородным в точке (x, y)
def is_same_color(pixel_color, target_color):
    return pixel_color == target_color

# Алгоритм заливки затравкой
def flood_fill(start_x, start_y, target_color, fill_color):
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack.pop()

        if 0 <= x < 400 and 0 <= y < 400:
            pixel_data = canvas.find_closest(x, y)
            pixel_color = canvas.itemcget(pixel_data, "fill")

            if is_same_color(pixel_color, target_color):
                canvas.itemconfig(pixel_data, fill=fill_color)
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

# Обработчики событий для рисования на холсте
def on_mouse_down(event):
    global is_drawing
    if not is_fill_mode:
        is_drawing = True
        drawn_elements.clear()
        start_x, start_y = event.x, event.y
        drawn_elements.append((start_x, start_y))
        add_drawn_pixel(start_x, start_y)

def on_mouse_move(event):
    global is_drawing
    if is_drawing and not is_fill_mode:
        x, y = event.x, event.y
        x_prev, y_prev = drawn_elements[-1]
        draw_line(x_prev, y_prev, x, y)
        drawn_elements[-1] = (x, y)
        add_drawn_pixel(x, y)

def on_mouse_up(event):
    global is_drawing
    is_drawing = False

canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_mouse_up)

# Обработчик события клика для запуска заливки затравкой
def on_fill_click(event):
    global is_fill_mode
    if is_fill_mode:
        if not drawn_elements:
            messagebox.showinfo("Error", "No lines drawn yet!")
            return
        x, y = event.x, event.y
        target_color = "white"  # Color outside the lines
        fill_color = "#ffff00"  # Yellow
        flood_fill(x, y, target_color, fill_color)

canvas.bind("<Button-3>", on_fill_click)

# Обработчики для кнопок выбора режима
def set_draw_mode():
    global is_fill_mode
    is_fill_mode = False

def set_fill_mode():
    global is_fill_mode
    is_fill_mode = True

draw_mode_btn = tk.Button(root, text="Draw Mode", command=set_draw_mode)
draw_mode_btn.pack(side="left")

fill_mode_btn = tk.Button(root, text="Fill Mode", command=set_fill_mode)
fill_mode_btn.pack(side="left")

# Обработчик для кнопки очистки холста
def clear_canvas():
    canvas.delete("all")
    drawn_elements.clear()

clear_btn = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_btn.pack(side="left")

root.mainloop()
