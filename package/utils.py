

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
