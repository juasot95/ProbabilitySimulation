import pygame
from typing import Callable


class Text(pygame.sprite.Sprite):
    def __init__(self, text, _vars=lambda: dict(), size=36, color='#CCCCCC'):
        super().__init__()
        self.text = text
        self.vars = _vars
        self.formatted_text = self.current_text

        self.font = pygame.font.Font(None, size)
        self.color = color
        self.image = self.font.render(f'{self.current_text}', 1, self.color)
        self.rect = self.image.get_rect()

    @property
    def current_text(self) -> str:
        self.vars: Callable[[], dict[str: str]]
        return self.text.format(**self.vars())

    def update(self):
        if not self.vars():
            return
        if self.formatted_text == self.current_text:
            return
        self.formatted_text = self.current_text
        self.image = self.font.render(f'{self.current_text}', 1, self.color)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class PercentText(Text):
    def __init__(self, *args, color='#BBBBBB', size=24, **kwargs):
        Text.__init__(self, *args, size=size, **kwargs)
        self.color = color


class RewardText(PercentText):
    def __init__(self, *args, color='#BBEEBB', size=36, **kwargs):
        Text.__init__(self, *args, size=size, **kwargs)
        self.color = color

