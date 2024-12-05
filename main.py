import pygame
import time
from package.path import Path


print('starting program...')
screen = pygame.display.set_mode((480, 480))
running = True

path = Path((200, 50), (200, 350))

t0 = time.time()
dt = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    path.update(dt)
    path.render(screen)
    pygame.display.flip()
    screen.fill('#000000')
    dt = -(t0 - (t0 := time.time()))

pygame.quit()
