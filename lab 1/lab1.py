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

# Инициализация Pygame
pygame.init()

# Установка размеров окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Задание цвета
white = (255, 255, 255)
black = (0, 0, 0)

lines = []
start_pos = (0, 0)  # Initialize start_pos

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получение координат курсора
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Рисование линии при нажатии левой кнопки мыши
    if pygame.mouse.get_pressed()[0]:
        start_pos = (mouse_x, mouse_y)
    else:
        end_pos = (mouse_x, mouse_y)
        lines.append((start_pos, end_pos))

    # Очистка экрана
    screen.fill(white)

    # Рисование вертикальной линии (фиксированная x-координата)
    pygame.draw.line(screen, black, (width // 2, 0), (width // 2, height), 2)

    # Отображение линий
    for line in lines:
        draw_line_bresenham(screen, black, line[0], line[1])

    # Отображение координат курсора
    font = pygame.font.Font(None, 36)
    text = font.render(f"Cursor: ({mouse_x}, {mouse_y})", True, black)
    screen.blit(text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

# Завершение программы
pygame.quit()
sys.exit()