import pygame
from package.utils import PercentText, RewardText, Text
from package.path import Path
from package.stats import Statistics


class Interface:
    def __init__(self, n=1, prob=0.5, speed=200):
        self.stats = Statistics()
        self.screen = pygame.display.set_mode((720, 480))
        self.path = Path((200, 75), (200, 425), stats=self.stats, prob=prob, speed=speed)
        self.stats.__init__(path=self.path)  # bind the Path with the Stat instance
        print(self.stats.optimizer.p_extremum)
        self.path.traffic.prob = self.stats.optimizer.p_max

        for i in range(n):
            self.path.traffic.add()

        # ___ -- Graphics Components -- ___
        prob = self.path.traffic.prob
        self.prob1_text = PercentText(prob)
        self.prob2_text = PercentText(prob*(1-prob))
        self.prob3_text = PercentText((1-prob)**2)
        self.reward1_text = RewardText(self.path.road1.reward)
        self.reward2_text = RewardText(self.path.road2.reward)
        self.reward3_text = RewardText(self.path.road3.reward)
        self.mean_reward_text = Text('Mean Reward : {mean_reward:.2f}',
                                     lambda: {'mean_reward': self.stats.mean_reward})
        self.expected_reward_text = Text('Expected Reward : {expected_reward:.2f}',
                                         lambda: {'expected_reward': self.stats.expected_reward})
        self.probability_text = Text('Probability: {prob:.2%}',
                                     lambda: {'prob': self.path.traffic.prob})
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
        # ___ -- Graphic Values -- ___
        pos = p0 + self.shift + pygame.Vector2(shift.x + 30, 0)
        self.mean_reward_text.rect.midleft = pos
        pos = self.mean_reward_text.rect.bottomleft
        self.expected_reward_text.rect.topleft = pos
        pos = self.expected_reward_text.rect.bottomleft
        self.probability_text.rect.topleft = pos

    def update_graphic_components(self):
        self.mean_reward_text.update()
        self.expected_reward_text.update()
        self.probability_text.update()

    def render_graphic_components(self):
        self.prob1_text.render(self.screen)
        self.prob2_text.render(self.screen)
        self.prob3_text.render(self.screen)
        self.reward1_text.render(self.screen)
        self.reward2_text.render(self.screen)
        self.reward3_text.render(self.screen)

        self.mean_reward_text.render(self.screen)
        self.expected_reward_text.render(self.screen)
        self.probability_text.render(self.screen)

    def update(self, dt):
        dt: float
        self.path.update(dt)
        self.update_graphic_components()

    def render(self):
        self.path.render(self.screen)
        self.render_graphic_components()
        pygame.display.flip()
        self.screen.fill('#000000')

    def tick(self, dt):
        dt: float
        self.update(dt)
        self.render()
