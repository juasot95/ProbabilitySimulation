import pygame
from package.car import Car
import random


class Traffic(list):
    def __init__(self, *args, path=None, probability=0.5):
        super().__init__(args)
        self.prob = probability
        if path is None:
            raise ValueError('The path parameter for the Traffic instance must be provided')
        self.path: "package.path.Path" = path  # NOQA

    def add(self) -> None:
        p = random.random
        if p() < self.prob:
            # summon car to road 1
            self.path.summon_car_to_road_n(1)
            pass
        elif p() < self.prob:
            # summon car to road 2
            self.path.summon_car_to_road_n(2)
            pass
        else:
            # summon car to road 3
            self.path.summon_car_to_road_n(3)
            pass

    def draw(self, surface: pygame.Surface):
        for car in self:
            car.draw(surface)

    def update(self, dt):
        dt: float
        for car in self:
            car.move(dt)
