import pygame
from package.utils.text import Text


class Button:
    def __init__(self, x, y, w, h, interface, color='#454545', trigger_func=lambda: None):
        interface: 'package.interface.Interface'  # NOQA
        self.interface = interface
        self.path = self.interface.path
        self.optimizer = self.interface.stats.optimizer

        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.pressed = False
        self.trigger_func = trigger_func

    def set_prob(self, prob):
        self.path: 'package.path.Path'  # NOQA
        self.optimizer: 'package.stats.Optimizer'  # NOQA
        self.path.traffic.prob = prob

    @property
    def mouse_on(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def click(self) -> bool:
        return pygame.mouse.get_pressed()[0]

    def update(self):
        if self.pressed and not self.click:
            self.trigger_func()
        if self.click and self.mouse_on:
            self.pressed = True
        else:
            self.pressed = False

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=min(self.rect.size)//3)


class MaxButton(Button):
    def __init__(self, *args, color='#458545', **kwargs):
        Button.__init__(self, *args, color=color, **kwargs)
        self.text = Text('MAX')

    def update(self):
        if self.pressed and not self.click:
            # print('Max !!')
            self.path.traffic.prob = float(self.optimizer.p_max)
        Button.update(self)
        self.text.rect.center = self.rect.center

    def render(self, surface: pygame.Surface):
        Button.render(self, surface)
        self.text.render(surface)


class MinButton(Button):
    def __init__(self, *args, color='#854545', **kwargs):
        Button.__init__(self, *args, color=color, **kwargs)
        self.text = Text('MIN')

    def update(self):
        if self.pressed and not self.click:
            # print('Min !!')
            self.path.traffic.prob = float(self.optimizer.p_min)
        Button.update(self)
        self.text.rect.center = self.rect.center

    def render(self, surface: pygame.Surface):
        Button.render(self, surface)
        self.text.render(surface)


class RewardButton:
    def __init__(self, x, y, radius, interface, color='#454545', trigger_func=lambda: None):
        self.interface = interface
        self.trigger_func = trigger_func
        self.pressed = False

        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.color = color

    @property
    def mouse_rel_pos(self) -> pygame.Vector2:
        return pygame.Vector2(pygame.mouse.get_pos()) - self.pos

    @property
    def mouse_on(self) -> bool:
        return self.mouse_rel_pos.magnitude() < self.radius

    @property
    def click(self) -> bool:
        return pygame.mouse.get_pressed()[0]

    def update(self):
        if self.pressed and not self.click:
            self.trigger_func()
        if self.click and self.mouse_on:
            self.pressed = True
        else:
            self.pressed = False

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
