from typing import Optional, TextIO

from snr_core.context.stdout_consumer import StdOutConsumer, StdOutTask


class StdOut(StdOutConsumer):
    def __init__(self,
                 parent_name: str,
                 stdout: Optional[TextIO] = None
                 ) -> None:
        super().__init__(parent_name,
                         self.handler)
        self.stdout = stdout
        if self.stdout:
            self.stdout.flush()

    def handler(self, task: StdOutTask) -> None:
        if self.stdout:
            self.stdout.write(task.msg)
            if task.flush:
                self.stdout.flush()
