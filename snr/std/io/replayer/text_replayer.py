import threading

from snr.core.base import *

from .text_reader import TextReader

NAME_PREFIX = "text_replayer_"


class TextReplayer(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 filename: str,
                 data_name: str,
                 exit_when_done: bool
                 ) -> None:
        super().__init__(factory,
                         parent,
                         NAME_PREFIX + data_name,
                         tick_rate_hz=100)
        self.log.setLevel(logging.WARNING)
        self.task_handlers = {
            (TaskType.process_data, data_name): self.retire_data
        }
        self.data_name = data_name
        self.reader = TextReader(self, "text_replayer", filename)
        self.data_in_flight = threading.Event()
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.next_page: Optional[Page] = None

    def loop_handler(self) -> None:
        if not self.done:
            if not self.data_in_flight.is_set():
                line = self.reader.read()
                self.dbg("Read line %s", line)
                if line:
                    self.parent.store_data(self.data_name, line)
                elif not self.done:
                    self.dbg("Reader Done")
                    self.done = True
                    if self.exit_when_done:
                        self.dbg("Reader scheduling terminate task")
                        self.parent.schedule(task_terminate("replayer_done"))
            else:
                self.dbg("Data already in flight")

    def terminate(self) -> None:
        self.reader.close()

    def retire_data(self, t: Task, k: TaskId) -> SomeTasks:
        self.data_in_flight.clear()
        self.dbg("Data retired")
        return None
