import re


class Counter:
    def __init__(self, starting_value=0):
        self.value = starting_value

    def __call__(self, *args, **kwargs):
        self.value += 1

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.value}'

    def __format__(self, format_spec):
        if '>' in format_spec:
            def indentation(f_spec) -> int:
                match = re.search(r'.*>\s*(\d+)', f_spec)
                if match:
                    return int(match.group(1))  # Returns the sequence of numbers found
                return 0  # If nothing is found
            return repr(self).rjust(indentation(format_spec))
        return 'Nothing'


class Optimizer:
    """
    Source : https://www.desmos.com/calculator/ju7jv1zd4n?lang=fr
    """
    def __init__(self, path=None):
        self.path = path

    def expected_reward(self, p: float) -> float:
        return p*self.r1 + p*(1-p)*self.r2 + (1-p)**2*self.r3

    @property
    def r1(self) -> float:
        return self.path.road1.reward

    @property
    def r2(self) -> float:
        return self.path.road2.reward

    @property
    def r3(self) -> float:
        return self.path.road3.reward

    @property
    def p_extremum(self) -> float:
        if self.r2 == self.r3:
            return 0
        else:
            p = (self.r1 + self.r2 - self.r3*2) / (2*(self.r2 - self.r3))
            return p if 0 <= p <= 1 else 0

    @property
    def p_max(self) -> float:
        return max(0., 1, self.p_extremum, key=lambda x: self.expected_reward(x))

    @property
    def p_min(self) -> float:
        return min(0., 1, self.p_extremum, key=lambda x: self.expected_reward(x))

    @property
    def r_max(self) -> float:
        return self.expected_reward(self.p_max)

    @property
    def r_min(self) -> float:
        return self.expected_reward(self.p_min)


class Statistics:
    def __init__(self, path=None):
        self.path = path
        self.road1 = Counter()
        self.road2 = Counter()
        self.road3 = Counter()

        self.total_reward = 0

        self.optimizer = Optimizer(path)

    def __repr__(self):
        normal_info = 'mean_r={mean_reward:>5.2f}, expect_r={expected_reward:>5.2f}, {prob:>3.2%}'
        max_info = 'max_r = {max_reward:3.2f} (p={max_prob:.2%})'
        min_info = 'min_r = {min_reward:3.2f} (p={min_prob:.2%})'
        values = {'mean_reward': self.mean_reward, 'expected_reward': self.expected_reward,
                  'prob': self.path.traffic.prob,
                  'max_reward': self.optimizer.r_max, 'max_prob': self.optimizer.p_max,
                  'min_reward': self.optimizer.r_min, 'min_prob': self.optimizer.p_min}
        return '  |  '.join((normal_info, max_info, min_info)).format(**values)

    def __del__(self):
        self.reset()

    def reset(self):
        self.road1.__init__()
        self.road2.__init__()
        self.road3.__init__()
        self.total_reward = 0

    def add1_to_counter_n(self, n):
        n: int
        counter: Counter
        counter = (self.road1, self.road2, self.road3)[n-1]
        counter()
        # print(n, counter.value)

    @property
    def mean_reward(self) -> float:
        if (self.road1.value + self.road2.value + self.road3.value) == 0:
            return 0
        return self.total_reward / (self.road1.value + self.road2.value + self.road3.value)

    @property
    def expected_reward(self) -> float:
        self.path: 'package.path.Path'  # NOQA
        prob: float = self.path.traffic.prob
        return self.path.road1.reward*prob + self.path.road2.reward*prob*(1-prob) + self.path.road3.reward*(1-prob)**2

    def get_reward(self, n):
        n: int
        path: 'package.path.Path' = self.path  # NOQA
        reward = (path.road1, path.road2, path.road3)[n - 1].reward
        return reward

    def add_reward(self, n):
        n: int
        self.total_reward += self.get_reward(n)

    def update(self, n, path):
        n: int
        path: 'package.path.Path'  # NOQA
        self.add1_to_counter_n(n)
        self.add_reward(n)
