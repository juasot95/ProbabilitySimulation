import pygame
from package.path import Path
from package.stats import Statistics


class PercentText(pygame.sprite.Sprite):
    def __init__(self, value: float, size=24):
        super().__init__()
        self.value = value
        self.font = pygame.font.Font(None, size)
        self.color = '#BBBBBB'
        self.image = self.font.render(f'{self.value:.2%}', 1, self.color)
        self.rect = self.image.get_rect()

    def update(self, value):
        if value is None:
            return
        if value != self.value:
            self.value = value
            self.image = self.font.render(f'{self.value:.2%}', 1, self.color)
            self.rect = self.image.get_rect()

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class RewardText(pygame.sprite.Sprite):
    def __init__(self, value: float, size=36):
        super().__init__()
        self.value = value
        self.font = pygame.font.Font(None, size)
        self.color = '#BBEEBB'
        self.image = self.font.render(f'{self.value}', 1, self.color)
        self.rect = self.image.get_rect()

    def update(self, value):
        if value is None:
            return
        if value != self.value:
            self.value = value
            self.image = self.font.render(f'{self.value}', 1, self.color)
            self.rect = self.image.get_rect()

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class Interface:
    def __init__(self):
        self.stats = Statistics()
        self.screen = pygame.display.set_mode((720, 480))
        self.path = Path((200, 75), (200, 425), stats=self.stats)
        for i in ' '*50:
            self.path.traffic.add()
        # ___ -- Graphics Components -- ___
        prob = self.path.traffic.prob
        self.prob1_text = PercentText(prob)
        self.prob2_text = PercentText(prob*(1-prob))
        self.prob3_text = PercentText((1-prob)**2)
        self.reward1_text = RewardText(self.path.road1.reward)
        self.reward2_text = RewardText(self.path.road2.reward)
        self.reward3_text = RewardText(self.path.road3.reward)
        self.__init_graphic_components()

    def __init_graphic_components(self):
        shift = self.shift = pygame.Vector2(1, .5)
        p0 = self.path.starting_pos
        p1 = self.path.ending_pos
        spacing = (p1 - p0) / 4
        shift *= spacing.magnitude()

        # ___ -- Percents -- __
        pos = p0 + spacing + self.shift/2
        self.prob1_text.rect.center = pos
        pos = p0 + spacing*2 + self.shift/2
        self.prob2_text.rect.center = pos
        pos = p0 + spacing*3 + self.shift/2
        self.prob3_text.rect.center = pos
        # ___ -- Rewards -- ___
        pos = p0 + spacing + self.shift
        self.reward1_text.rect.center = pos
        pos = p0 + spacing*2 + self.shift
        self.reward2_text.rect.center = pos
        pos = p0 + spacing*3 + self.shift
        self.reward3_text.rect.center = pos

    def update(self, dt):
        dt: float
        self.path.update(dt)

    def render_graphic_components(self):
        self.prob1_text.render(self.screen)
        self.prob2_text.render(self.screen)
        self.prob3_text.render(self.screen)
        self.reward1_text.render(self.screen)
        self.reward2_text.render(self.screen)
        self.reward3_text.render(self.screen)

    def render(self):
        self.path.render(self.screen)
        self.render_graphic_components()
        pygame.display.flip()
        self.screen.fill('#000000')

    def tick(self, dt):
        dt: float
        self.update(dt)
        self.render()
