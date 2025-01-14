import pygame
import random

pygame.init()

width, height = 800, 600
fps = 60
radius = 20


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Circle:
    def __init__(self):
        self.x = random.randint(radius, width - radius)
        self.y = random.randint(radius, height - radius)
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])
        self.radius = radius
        self.color = random_color()

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= self.radius or self.x >= width - self.radius:
            self.dx *= -1
            self.color = random_color()
        if self.y <= self.radius or self.y >= height - self.radius:
            self.dy *= -1
            self.color = random_color()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def collision(self, other):
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        if distance < self.radius * 2:
            return True
        return False

    def handle_collision(self, other):
        if self.collision(other):
            self.dx *= -1
            self.dy *= -1
            self.color = random_color()
            other.dx *= -1
            other.dy *= -1
            other.color = random_color()


def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bouncing Circles")
    clock = pygame.time.Clock()

    num_circle = random.randint(5, 20)
    circles = [Circle() for _ in range(num_circle)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i in range(len(circles)):
            circles[i].move()
            for j in range(i + 1, len(circles)):
                circles[i].handle_collision(circles[j])
            circles[i].draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
