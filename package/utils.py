import pygame
from typing import Callable


class Coordinates:
    def __init__(self, /, x=0, y=0) -> None:
        x: int
        y: int
        self.x = x
        self.y = y

    def __getitem__(self, item) -> int:
        if isinstance(item, int):
            match item:
                case 0: return self.x
                case 1: return self.y
                case _: raise IndexError(f'You should pass either 1 or 0 not {item}')
        if isinstance(item, str):
            match item:
                case 'x': return self.x
                case 'y': return self.y
                case _: raise KeyError(
                    f'You can only pass \'x\', or \'y\' as a key but you passed {repr(item)}')
        raise ValueError(f'You can only pass either an int or a str...')


class PercentText(pygame.sprite.Sprite):
    def __init__(self, value: float, size=24):
        super().__init__()
        self.value = value
        self.font = pygame.font.Font(None, size)
        self.color = '#BBBBBB'
        self.image = self.font.render(f'{self.value:.2%}', 1, self.color)
        self.rect = self.image.get_rect()

    @property
    def new_text(self) -> str:
        return f'{self.value:.2%}'

    def update(self, value):
        if value is None:
            return
        if value != self.value:
            self.value = value
            self.image = self.font.render(self.new_text, 1, self.color)
            self.rect = self.image.get_rect()

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class RewardText(PercentText):
    def __init__(self, value: float, size=36):
        pygame.sprite.Sprite.__init__(self)
        PercentText.__init__(self, value=value, size=size)
        self.value = value
        self.color = '#BBEEBB'
        self.image = self.font.render(f'{self.value}', 1, self.color)
        self.rect = self.image.get_rect()

    @property
    def new_text(self) -> str:
        return f'{self.value}'


class Text(pygame.sprite.Sprite):
    def __init__(self, text, _vars=lambda: dict(), size=36):
        super().__init__()
        self.text = text
        self.vars = _vars
        self.formatted_text = self.current_text

        self.font = pygame.font.Font(None, size)
        self.color = '#CCCCCC'
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

