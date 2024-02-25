import pygame
import sys

# Функция для отрисовки эллипса по методу Брезенхема
def draw_ellipse(screen, x, y, a, b, color):
    a_sqr = a * a
    b_sqr = b * b
    two_a_sqr = 2 * a_sqr
    two_b_sqr = 2 * b_sqr
    x0, y0 = 0, b
    dx, dy = 0, two_a_sqr * b
    err = 0
    while dy >= 0:
        pygame.draw.circle(screen, color, (x + x0, y + y0), 1)
        pygame.draw.circle(screen, color, (x - x0, y + y0), 1)
        pygame.draw.circle(screen, color, (x - x0, y - y0), 1)
        pygame.draw.circle(screen, color, (x + x0, y - y0), 1)
        e2 = 2 * err - dy - 1
        if e2 <= 0:
            x0 += 1
            dx += two_b_sqr
            err += dx
        if e2 >= 0:
            y0 -= 1
            dy -= two_a_sqr
            err -= dy

# Функция для отображения окна Pygame
def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ellipse Drawer")

    center = (width // 2, height // 2)  # Стартовое значение центра
    a, b = 0, 250  # Стартовые значения радиусов

    rotation = True

    clock = pygame.time.Clock()  # Создаем объект Clock

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((255, 255, 255))  # Очистка экрана белым цветом

            if rotation:
                a += 10
                if a == 250:
                    rotation = False
            else:
                a -= 10
                if a == 10:
                    rotation = True

            # Рисуем эллипс
            draw_ellipse(screen, center[0], center[1], a, b, (0, 0, 0))

            pygame.display.flip()

            clock.tick(60)  # Ограничение на 60 кадров в секунду

    except Exception as e:
        print("Произошла ошибка:", e)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
