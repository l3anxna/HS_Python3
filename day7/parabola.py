import pygame
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.info("Program started")

def f(x):
    return x ** 2

pygame.init()

w = 600
h = 600

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Plot Graph of y = x^2")

running = True

x_min = -2
x_max = 2
scale_x = w / (x_max - x_min)
max_y_value = f(x_max)
scale_y = h / max_y_value

previous_point = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for x in range(-200, 201):
        scaled_x = x / 100.0
        y = f(scaled_x)
        
        inverted_y = h - (y * scale_y) - 1
        pixel_x = int((scaled_x - x_min) * scale_x)

        if previous_point is not None:
            pygame.draw.line(screen, (255, 255, 255), previous_point, (pixel_x, inverted_y))

        previous_point = (pixel_x, inverted_y)

    pygame.display.flip()

pygame.quit()
