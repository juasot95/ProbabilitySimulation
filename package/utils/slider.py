import pygame


class Slider:
    def __init__(self, x, y, w, h, max_value=1, value_getter=lambda: None,
                 reset_func=lambda: None):
        self.reset_func = reset_func
        self.value_getter = value_getter
        self.pressed = False

        self.bg_color = pygame.Color('#666666')
        self.cursor_color = pygame.Color('#888888')
        self.rect = pygame.Rect(x, y, w, h)

        self.cursor_rect = pygame.Rect(0, 0, h//2, h)
        self.reset()

    @property
    def mouse_rel_pos(self) -> pygame.Vector2:
        return pygame.Vector2(pygame.mouse.get_pos()) - self.rect.topleft

    @property
    def mouse_on(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def click(self) -> bool:
        return pygame.mouse.get_pressed()[0]

    @property
    def value(self) -> float:
        value = self.cursor_rect.centerx / (self.rect.w-1)
        return min(max(0., value), 1)

    def reset(self):
        self.reset_func()
        if self.value_getter() is None:
            return
        prob = self.value_getter()  # NOQA
        self.cursor_rect.centerx = self.rect.w * prob - (prob > .5)  # NOQA

    def update(self):
        if self.value_getter() != self.value and self.value_getter() is not None:
            self.cursor_rect.centerx = self.value_getter()*self.rect.w  # NOQA
        if not self.mouse_on:
            if self.pressed:
                self.pressed = False
                self.cursor_rect.centerx = min(max(0, self.mouse_rel_pos.x), self.rect.w)
                self.reset()
            return
        if not self.click:
            if self.pressed:
                self.reset()
            self.pressed = False
            return
        self.pressed = True
        self.cursor_rect.centerx = self.mouse_rel_pos.x

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=min(self.rect.size)//3)
        pygame.draw.rect(surface, self.cursor_color,
                         (pygame.Vector2(self.rect.topleft)+self.cursor_rect.topleft,
                          self.cursor_rect.size),
                         border_radius=min(self.cursor_rect.size)//2)

