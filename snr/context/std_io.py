from sys import stdin, stdout
from typing import Callable, TextIO, Tuple, Union

from snr.utils.consumer import Consumer

PromptResult = str
PromptRequestCallback = Callable[[PromptResult], None]

StdOutTask = str
StdInTask = Tuple[str, PromptRequestCallback]
StdIoTask = Union[StdOutTask, StdInTask]


def isinstance_StdInTask(task: StdIoTask) -> bool:
    return (isinstance(task, Tuple)
            and isinstance(task[1], PromptRequestCallback))


class StdIo(Consumer):
    def __init__(self, parent_name: str) -> None:
        super().__init__(parent_name, self.stdio_handler, 0)
        self.stdin: TextIO = stdin
        self.stdout: TextIO = stdout

    def stdio_handler(self, task: StdIoTask) -> None:
        if isinstance(task, StdOutTask):
            self.output_handler(task)
        elif isinstance_StdInTask(task):
            self.input_handler(task)
        else:
            print(f"Invalid StdIOTask: {str(task)}")

    def flush(self):
        self.catch_up("flush")
        self.stdout.flush()

    def output_handler(self, s: StdOutTask) -> None:
        self.stdout.write(s)

    def input_handler(self, t: StdInTask) -> None:
        prompt: str = t[0]
        callback: PromptRequestCallback = t[1]
        self.flush()
        self.stdout.write(prompt)
        self.stdout.flush()
        result = stdin.readline()
        callback(result)
