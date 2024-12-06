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


class Statistics:
    def __init__(self, path=None):
        self.path = path
        self.road1 = Counter()
        self.road2 = Counter()
        self.road3 = Counter()

        self.total_reward = 0

    def add1_to_counter_n(self, n):
        n: int
        counter: Counter
        counter = (self.road1, self.road2, self.road3)[n-1]
        counter()
        # print(n, counter.value)

    def add_reward(self, n, path):
        n: int
        path: 'package.path.Path'  # NOQA
        reward = (path.road1, path.road2, path.road3)[n-1].reward
        self.total_reward += reward

    def update(self, n, path):
        n: int
        path: 'package.path.Path'  # NOQA
        self.add1_to_counter_n(n)
        self.add_reward(n, path)

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

    def __repr__(self):
        return f'1: {self.road1:>3}, 2: {self.road2:>3}, 3: {self.road3:>3}'\
            f'  ({self.mean_reward = :.2f}, {self.expected_reward = :.2f})'  # NOQA: E203
