import pygame
import sys


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Circle")

radius = 20
x, y = 100, 100
dx, dy = 2, 2


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    x += dx
    y += dy

    if x - radius < 0 or x + radius > width:
        dx *= -1
    if y - radius < 0 or y + radius > height:
        dy *= -1

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

    pygame.display.flip()

    pygame.time.delay(10)
