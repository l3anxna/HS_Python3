import pygame
import math

pygame.init()

w = 600
h = 600

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Plot Graph of y = sin(x)")

running = True

x_min = -6
x_max = 6
scale_x = w / (x_max - x_min)
scale_y = h / 2

previous_point = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for x in range(-600, 601):
        scaled_x = x / 100.0
        y = math.sin(scaled_x)
        
        inverted_y = h / 2 - (y * scale_y)
        pixel_x = int((scaled_x - x_min) * scale_x)

        if previous_point is not None and abs(pixel_x - previous_point[0]) < 2:
            pygame.draw.line(screen, (255, 255, 255), previous_point, (pixel_x, inverted_y))

        previous_point = (pixel_x, inverted_y)

    pygame.display.flip()

pygame.quit()
