import random
from typing import Iterable


class NameList:
    seed = 0

    def __init__(self, names: Iterable, repetition=1, default_count=1, priority=0):
        base_names = [str(name) for name in names]
        self.names = []
        for i in range(repetition):
            self.names += base_names[: int(len(base_names) / 10) + 1]
        self._loc = 0
        self.seed = -1
        self.shuffle()

        self.count = default_count
        self.priority = priority

    def shuffle(self):
        self.seed = NameList.seed
        NameList.seed += 1
        random.seed(self.seed)
        random.shuffle(self.names)
        self.loc = 0

    @property
    def loc(self):
        self._loc = (self._loc + 1) % len(self.names)
        return self._loc

    @loc.setter
    def loc(self, new_loc: int):
        self._loc = new_loc % len(self.names)

    def get(self, n: int = 1) -> list[str]:
        namerator = iter(self)
        return [next(namerator) for __ in range(n)]

    def __len__(self):
        return len(self.names)

    def __next__(self):
        return self.names[self.loc]

    def __iter__(self):
        return self

    def __str__(self):
        return f"{', '.join(self.get(self.count))}"

    def __repr__(self):
        return f"<NameList[{len(self)}] ({','.join(self.names[:3])})>"
