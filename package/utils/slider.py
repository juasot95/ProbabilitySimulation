import pygame


class Slider:
    def __init__(self, x, y, w, h, max_value=1):
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
        value = self.cursor_rect.centerx
        return value/(self.rect.w-1)

    def reset(self):
        self.cursor_rect.center = self.rect.midleft

    def update(self):
        if not self.click:
            if self.pressed:
                print(self.value)
                pass
            self.pressed = False
            return
        if not self.mouse_on:
            return
        self.pressed = True
        self.cursor_rect.centerx = self.mouse_rel_pos.x

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=min(self.rect.size)//3)
        pygame.draw.rect(surface, self.cursor_color,
                         (pygame.Vector2(self.rect.topleft)+self.cursor_rect.topleft,
                          self.cursor_rect.size),
                         border_radius=min(self.cursor_rect.size)//2)

