from dataclasses import dataclass
from typing import Callable

from snr_core.utils.consumer import Consumer


@dataclass
class StdOutTask:
    msg: str
    flush: bool


STDIO_NAME_SUFFIX = "_stdio"
ONE_HUNDRED_MICROSECONDS = 0.0001


class StdOutConsumer(Consumer[StdOutTask]):
    def __init__(self,
                 parent_name: str,
                 handler: Callable[[StdOutTask], None],
                 inner_print: Callable[[str], None] = print
                 ) -> None:
        super().__init__(parent_name + STDIO_NAME_SUFFIX,
                         handler,
                         ONE_HUNDRED_MICROSECONDS,
                         inner_print)
        self.handler = handler

    def print(self, msg: str) -> None:
        self.put(StdOutTask(msg, True))

    def join_from(self, joiner: str):
        self.flush()
        self.handler(StdOutTask(f"{joiner} joining stdio\n", False))
        super().join_from(joiner)
