from package.utils import Coordinates
import pygame


class Car:
    def __init__(self, pos, /, radius=10, *, path, traffic,
                 color='#D58635', destroy=True, run_when_destroyed=lambda: 0) -> None:
        pos: pygame.Vector2
        radius: int
        path: list[Coordinates, ...]
        color: str
        self.pos = pos
        self.radius = radius
        self.path = path
        self.traffic = traffic
        self.color = color

        self.speed = 300  # pxl/s

        self.destroy = destroy
        self.run_when_destroyed = run_when_destroyed

    def set_speed(self, speed: int) -> None:
        self.speed = speed

    def move(self, dt) -> None:
        dt: float
        if not self.path:
            if self.destroy:
                self.run_when_destroyed()
                self.traffic.remove(self)
                del self
                return
            else:
                return
        target_pos = pygame.Vector2(self.path[0])

        if (self.pos - target_pos).magnitude_squared() > (self.speed*dt)**2:
            self.pos += (target_pos-self.pos).normalize()*self.speed*dt
        else:
            self.pos = target_pos
            self.path.pop(0)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, color=self.color, center=self.pos, radius=self.radius)

