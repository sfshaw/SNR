import time


class Timer:
    def __init__(self):
        self.start_time = time.time()

    def current(self) -> float:
        return time.time() - self.start_time
