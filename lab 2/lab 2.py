import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

font = pygame.font.Font(None, 24)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Алгоритм Брезенхема")

clock = pygame.time.Clock()

def draw_circle(center, radius):
    x, y = center

    d = 3 - 2 * radius
    points = []
    x_values = []
    y_values = []
    while x <= y:
        points.append((x, y))
        points.append((-x, y))
        points.append((x, -y))
        points.append((-x, -y))
        points.append((y, x))
        points.append((-y, x))
        points.append((y, -x))
        points.append((-y, -x))
        if d > 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    
    for point in points:
        x_values.append(point[0] + center[0])
        y_values.append(point[1] + center[1])

    return x_values, y_values

def main():
    center = (WIDTH // 2, HEIGHT // 2)
    radius = 50
    while True:
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                center = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    radius += 5
                elif event.key == pygame.K_DOWN:
                    radius -= 5
                    if radius < 5:
                        radius = 5

        x_values, y_values = draw_circle(center, radius)
        
        for i in range(len(x_values)):
            pygame.draw.circle(screen, black, (x_values[i], y_values[i]), 1)
        
        pygame.draw.circle(screen, red, center, radius, 1)

        text_surface = font.render("Радиус: {}".format(radius), True, black)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()