from typing import Deque


class MovingAvgFilter:
    def __init__(self, backing_deque: Deque[float]):
        self.deque = backing_deque

    def update(self, value: float) -> None:
        self.deque.append(value)

    def avg(self) -> float:
        n = len(self.deque)
        if n == 0:
            return 0
        return sum(self.deque) / n
