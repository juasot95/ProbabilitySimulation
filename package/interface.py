import pygame
from package.path import Path
from package.stats import Statistics


class Interface:
    def __init__(self):
        self.stats = Statistics()
        self.screen = pygame.display.set_mode((720, 480))
        self.path = Path((200, 75), (200, 425), stats=self.stats)
        for i in ' '*1:
            self.path.traffic.add()

    def update(self, dt):
        dt: float
        self.path.update(dt)

    def render(self):
        self.path.render(self.screen)
        pygame.display.flip()
        self.screen.fill('#000000')

    def tick(self, dt):
        dt: float
        self.update(dt)
        self.render()
