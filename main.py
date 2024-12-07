import pygame
import time
from package.path import Path
from package.interface import Interface


print('starting program...')

running = True
interface = Interface(50, 0.55, rewards=(3, 5, 0), speed=500)
clock = pygame.time.Clock()

t0 = time.time()
dt = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    interface.tick(dt)
    clock.tick(120)
    dt = -(t0 - (t0 := time.time()))

pygame.quit()
