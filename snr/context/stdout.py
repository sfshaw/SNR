from sys import stdout
from dataclasses import dataclass
from typing import Optional, TextIO

from snr.utils.consumer import Consumer


@dataclass
class StdOutTask:
    msg: str
    flush: bool


ONE_HUNDRED_MICROSECONDS = 0.0001
STDIO_NAME_SUFFIX = "_stdio"


class StdOut(Consumer[StdOutTask]):
    def __init__(self, parent_name: str) -> None:
        super().__init__(parent_name + STDIO_NAME_SUFFIX,
                         self.handler,
                         ONE_HUNDRED_MICROSECONDS)
        self.stdout: TextIO = stdout
        self.stdout.flush()

    def handler(self, task: StdOutTask) -> None:
        if isinstance(task, str):
            print(f"Task is str, not Task: {task}")

        self.stdout.write(task.msg)
        if task.flush:
            self.stdout.flush()

    def print(self, msg: str) -> None:
        self.put(StdOutTask(msg, True))

    def join_from(self, joiner: str, timeout: Optional[float] = None):
        self.stdout.write(f"{joiner} joining stdio\n")
        self.flush()
        super().join_from(joiner)
