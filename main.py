import pygame
import time
from package.path import Path
from package.interface import Interface


print('starting program...')

running = True
interface = Interface()

t0 = time.time()
dt = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    interface.tick(dt)
    dt = -(t0 - (t0 := time.time()))

pygame.quit()
