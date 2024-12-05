import pygame
from package.car import Car, Traffic


class Road:
    def __init__(self, starting_pos, ending_pos):
        starting_pos: tuple[int | float, int | float]
        ending_pos: tuple[int | float, int | float]
        self.starting_pos = pygame.Vector2(starting_pos)
        self.ending_pos = pygame.Vector2(ending_pos)

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, '#555555', self.starting_pos, self.ending_pos, width=10)
        pygame.draw.circle(surface, '#BBBBBB', center=self.starting_pos, radius=15)
        pygame.draw.circle(surface, '#DD5544', center=self.ending_pos, radius=20)


class Path(Road):
    def __init__(self, starting_pos, ending_pos):
        starting_pos: tuple[int | float, int | float]
        ending_pos: tuple[int | float, int | float]
        super().__init__(starting_pos, ending_pos)

        self.shift = pygame.Vector2(1, .5)

        self.road1 = self.road2 = self.road3 = Road((0, 0), (0, 0))
        self.__init_roads()

        self.cars = Traffic(
            Car((200, 200), path=[(200, 200), (200, 300), (200, 200), (200, 300)]),
            Car((200, 50), path=[(200, 200), (200, 300), (200, 200), (200, 300)]))

    def __init_roads(self):
        p0 = self.starting_pos
        p1 = self.ending_pos
        spacing = (p1-p0)/4
        self.shift *= spacing.magnitude()
        self.road1 = Road(p0+spacing, p0+spacing + self.shift)
        self.road2 = Road(p0+spacing*2, p0+spacing*2 + self.shift)
        self.road3 = Road(p0+spacing*3, p0+spacing*3 + self.shift)

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, '#555555',
                         pygame.Rect(self.starting_pos.x-5, self.starting_pos.y, 10,
                                     (self.ending_pos-self.starting_pos).magnitude()*.75))
        pygame.draw.circle(surface, '#44BB77', center=self.starting_pos, radius=20)
        self.road1.render(surface)
        self.road2.render(surface)
        self.road3.render(surface)
        self.cars.draw(surface)

    def update(self, dt):
        dt: float
        self.cars.update(dt)

