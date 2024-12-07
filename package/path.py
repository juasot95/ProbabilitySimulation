import pygame
from package.traffic import Traffic, Car
from package.stats import Statistics
from random import random


class Road:
    def __init__(self, starting_pos, ending_pos, reward=None):
        starting_pos: tuple[int | float, int | float]
        ending_pos: tuple[int | float, int | float]
        reward: float
        self.starting_pos = pygame.Vector2(starting_pos)
        self.ending_pos = pygame.Vector2(ending_pos)
        if reward is None:
            self.reward = random()*10
        else:
            self.reward = reward

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, '#555555', self.starting_pos, self.ending_pos, width=10)
        pygame.draw.circle(surface, '#BBBBBB', center=self.starting_pos, radius=15)
        pygame.draw.circle(surface, '#DD5544', center=self.ending_pos, radius=20)


class Path(Road):
    def __init__(self, starting_pos, ending_pos, stats=None, prob=0.5, speed=200, rewards=(3, 5, 0)):
        starting_pos: tuple[int | float, int | float]
        ending_pos: tuple[int | float, int | float]
        super().__init__(starting_pos, ending_pos)

        self.shift = pygame.Vector2(1, .5)

        self.road1 = self.road2 = self.road3 = Road((0, 0), (0, 0))
        self.__init_roads(rewards)

        self.traffic = Traffic(path=self, probability=prob)
        self.stats = stats or Statistics(self)
        self.stats.__init__(self)
        self.speed = speed

    def __init_roads(self, rewards=(3, 5, 0)):
        p0 = self.starting_pos
        p1 = self.ending_pos
        spacing = (p1-p0)/4
        self.shift *= spacing.magnitude()
        self.road1 = Road(p0+spacing, p0+spacing + self.shift, reward=rewards[0])
        self.road2 = Road(p0+spacing*2, p0+spacing*2 + self.shift, reward=rewards[1])
        self.road3 = Road(p0+spacing*3, p0+spacing*3 + self.shift, reward=rewards[2])

    def summon_car_to_road_n(self, n):
        n: int

        def destroy_function():
            # print('Destroyed !!')
            # print(self.stats)
            self.stats.update(n, self)
            self.traffic.add()
        road = (self.road1, self.road2, self.road3)[n-1]
        path = [self.starting_pos, road.starting_pos, road.ending_pos]
        car = Car(self.starting_pos, speed=self.speed, path=path,
                  traffic=self.traffic, run_when_destroyed=destroy_function)
        self.traffic.append(car)

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, '#555555',
                         pygame.Rect(self.starting_pos.x-5, self.starting_pos.y, 10,
                                     (self.ending_pos-self.starting_pos).magnitude()*.75))
        pygame.draw.circle(surface, '#44BB77', center=self.starting_pos, radius=20)
        self.road1.render(surface)
        self.road2.render(surface)
        self.road3.render(surface)
        self.traffic.draw(surface)

    def update(self, dt):
        dt: float
        self.traffic.update(dt)
        # print(self.traffic.prob)

