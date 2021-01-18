from sys import stdout
from typing import TextIO

from snr_core.context.stdout_consumer import StdOutConsumer, StdOutTask


class StdOut(StdOutConsumer):
    def __init__(self, parent_name: str) -> None:
        super().__init__(parent_name,
                         self.handler)
        self.stdout: TextIO = stdout
        self.stdout.flush()

    def handler(self, task: StdOutTask) -> None:
        self.stdout.write(task.msg)
        if task.flush:
            self.stdout.flush()
