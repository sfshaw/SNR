from snr.context.stdout import STDIO_NAME_SUFFIX, StdOutTask
from typing import Optional

from snr.utils.consumer import Consumer


ONE_HUNDRED_MICROSECONDS = 0.0001


class SilentStdOut(Consumer[StdOutTask]):
    def __init__(self, parent_name: str) -> None:
        super().__init__(parent_name + STDIO_NAME_SUFFIX,
                         self.handler,
                         ONE_HUNDRED_MICROSECONDS)

    def handler(self, task: StdOutTask) -> None:
        if isinstance(task, str):
            print(f"Task is str, not Task: {task}")

    def print(self, msg: str) -> None:
        self.put(StdOutTask(msg, True))

    def join_from(self, joiner: str, timeout: Optional[float] = None):
        self.flush()
        super().join_from(joiner)
