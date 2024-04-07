import tkinter as tk

# Создаем окно
root = tk.Tk()
root.title("Draw Rectangles and Lines")

# Создаем холст
canvas = tk.Canvas(root, width=800, height=600, borderwidth=1, relief="solid")
canvas.pack()

# Переменные для хранения состояния рисования
is_drawing_rect = False
is_drawing_line = False
start_point = {}
end_point = {}
rectangle = {}
x1, y1, x2, y2 = 0, 0, 0, 0

# Обработчик события нажатия кнопки мыши
def mouse_down(event):
    global is_drawing_rect, is_drawing_line, start_point, x1, y1
    if not is_drawing_rect and not is_drawing_line:
        is_drawing_rect = True
        start_point = {"x": event.x, "y": event.y}
        x1, y1 = event.x, event.y

# Обработчик события перемещения мыши
def mouse_move(event):
    global rectangle
    if is_drawing_rect and not is_drawing_line:
        current_point = {"x": event.x, "y": event.y}
        x = min(start_point["x"], current_point["x"])
        y = min(start_point["y"], current_point["y"])
        width = abs(start_point["x"] - current_point["x"])
        height = abs(start_point["y"] - current_point["y"])
        rectangle = {"x": x, "y": y, "width": width, "height": height}
        draw()

# Обработчик события отпускания кнопки мыши
def mouse_up(event):
    global is_drawing_rect, is_drawing_line, x2, y2, start_point
    if is_drawing_rect:
        is_drawing_rect = False
        is_drawing_line = True
        x2, y2 = event.x, event.y
        start_point = {}

# Обработчик события клика мыши
def mouse_click(event):
    global start_point, end_point, x1, y1, x2, y2
    if is_drawing_line:
        if not start_point:
            start_point = {"x": event.x, "y": event.y}
        else:
            end_point = {"x": event.x, "y": event.y}
            # Определяем границы прямоугольника
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)
            # Находим точки пересечения линии с границами прямоугольника
            start = find_ends(start_point, end_point, left, top, right, bottom)
            end = find_ends(end_point, start_point, left, top, right, bottom)
            # Рисуем только сегмент линии, находящийся внутри прямоугольника
            if start and end:
                canvas.create_line(start["x"], start["y"], end["x"], end["y"], fill="black")
            start_point = {}
            end_point = {}

# Метод для нахождения точки пересечения линии с границами прямоугольника
def find_ends(line_start, line_end, rect_left, rect_top, rect_right, rect_bottom):
    dx = abs(line_end["x"] - line_start["x"])
    dy = abs(line_end["y"] - line_start["y"])
    sx = 1 if line_start["x"] < line_end["x"] else -1
    sy = 1 if line_start["y"] < line_end["y"] else -1
    err = dx - dy

    x = line_start["x"]
    y = line_start["y"]

    while True:
        if (x >= rect_left and x <= rect_right and y >= rect_top and y <= rect_bottom):
            return {"x": x, "y": y}
        if (x == line_end["x"] and y == line_end["y"]):
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    return None

# Метод для отрисовки прямоугольников и текущего состояния холста
def draw():
    canvas.delete("all")
    if rectangle:
        canvas.create_rectangle(rectangle["x"], rectangle["y"], rectangle["x"] + rectangle["width"], 
                                rectangle["y"] + rectangle["height"], outline="green")

# Привязываем обработчики событий
canvas.bind("<Button-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_move)
canvas.bind("<ButtonRelease-1>", mouse_up)
canvas.bind("<Button-3>", mouse_click)

root.mainloop()
