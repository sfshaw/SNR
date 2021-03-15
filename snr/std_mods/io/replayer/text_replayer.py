import logging
import threading
from typing import Optional

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from .text_reader import TextReader

NAME_PREFIX = "text_replayer_"


class TextReplayer(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 filename: str,
                 data_key: DataKey,
                 exit_when_done: bool
                 ) -> None:
        super().__init__(factory,
                         parent,
                         NAME_PREFIX + data_key,
                         max_tick_rate_hz=100)
        self.log.setLevel(logging.WARNING)
        self.task_handlers = {
            (TaskType.process_data, data_key): self.retire_data
        }
        self.data_key = data_key
        self.reader = TextReader(self, "text_replayer", filename)
        self.data_in_flight = threading.Event()
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.next_page: Optional[Page] = None

    def setup(self) -> None:
        self.reader.open()

    def loop(self) -> None:
        if not self.done:
            if not self.data_in_flight.is_set():
                line = self.reader.read()
                self.dbg("Read line %s", line)
                if line:
                    self.parent.store_data(self.data_key, line)
                elif not self.done:
                    self.dbg("Reader Done")
                    self.done = True
                    if self.exit_when_done:
                        self.dbg("Reader scheduling terminate task")
                        self.schedule(tasks.terminate("replayer_done"))
            else:
                self.dbg("Data already in flight")

    def halt(self) -> None:
        self.reader.close()

    def terminate(self) -> None:
        self.reader.close()

    def retire_data(self, t: Task, k: TaskId) -> SomeTasks:
        self.data_in_flight.clear()
        self.dbg("Data retired")
        return None
