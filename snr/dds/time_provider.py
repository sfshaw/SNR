from time import time


class TimeProvider:

    def __init__(self):
        self.start_time = time()

    def current(self) -> float:
        now = time()
        return self.start_time - now
