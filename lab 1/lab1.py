import pygame
import sys

def draw_line_bresenham(screen, color, start, end):
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    error = dx - dy

    points = []

    while x1 != x2 or y1 != y2:
        points.append((x1, y1))
        e2 = 2 * error
        if e2 > -dy:
            error -= dy
            x1 += sx
        if e2 < dx:
            error += dx
            y1 += sy

    points.append((x2, y2))

    for point in points:
        pygame.draw.circle(screen, color, point, 1)

def draw_line_dda(screen, color, start, end):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    if max(abs(dx), abs(dy)) != 0:
        steps = max(abs(dx), abs(dy))
    else:
        steps = 1

    x_increment = dx / steps
    y_increment = dy / steps

    x = x1
    y = y1

    for _ in range(steps + 1):
        pygame.draw.circle(screen, color, (int(x), int(y)), 1)
        x += x_increment
        y += y_increment

# Инициализация Pygame
pygame.init()

# Установка размеров окна
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))

# Задание цвета
white = (255, 255, 255)
black = (0, 0, 0)

lines = []
start_pos = (0, 0)  # Initialize start_pos
drawing = False

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not drawing:
                start_pos = event.pos
                drawing = True
            else:
                end_pos = event.pos
                drawing = False
                lines.append((start_pos, end_pos))

    # Получение координат курсора
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Очистка экрана
    screen.fill(white)

    # Рисование вертикальной линии (фиксированная x-координата)
    pygame.draw.line(screen, black, (width // 2, 0), (width // 2, height), 2)

    # Отображение линий
    for line in lines:
        draw_line_bresenham(screen, black, line[0], line[1])
        draw_line_dda(screen, black, (line[0][0] + 600, line[0][1]), (line[1][0] + 600, line[1][1]))

    # Отображение координат курсора
    font = pygame.font.Font(None, 36)
    text = font.render(f"Cursor: ({mouse_x}, {mouse_y})", True, black)
    screen.blit(text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

# Завершение программы
pygame.quit()
sys.exit()