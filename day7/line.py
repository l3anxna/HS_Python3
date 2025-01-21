import pygame
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.info("Program started")

def f(x):
    return x

pygame.init()

w = 600
h = 600

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Draw Graph of y = x")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for x in range(w):
        y = f(x)
        inverted_y = h - y - 1
        if 0 <= inverted_y < h:
            screen.set_at((x, inverted_y), (255, 255, 255))

    pygame.display.flip()

pygame.quit()
