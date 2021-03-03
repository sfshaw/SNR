import threading
import time

from snr.core.base import *

from .page_reader import PageReader


class Replayer(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 filename: str,
                 exit_when_done: bool,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "replayer",
                         tick_rate_hz=5000)
        self.task_handlers: TaskHandlerMap = {
            TaskType.process_data: self.retire_data
        }
        self.reader = PageReader(self, "page_reader", filename)
        self.data_in_flight = threading.Event()
        self.last_data: Optional[DataKey] = None
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.next_page: Optional[Page] = None

    def setup(self) -> None:
        self.parent.store_data(f"{self.name}_pages_in_flight",
                               0,
                               process=False)

    def loop_handler(self) -> None:
        if not self.done and not self.data_in_flight.is_set():
            page = self.reader.read()
            if page:
                self.wait(page)
                self.parent.store_page(page)
                self.data_in_flight.set()
                self.last_data = page.key
            elif not self.done:
                self.dbg("Reader Done")
                self.done = True
                if self.exit_when_done:
                    self.dbg("Reader scheduling terminate task")
                    self.parent.schedule(task_terminate("replayer_done"))

    def terminate(self) -> None:
        self.reader.close()

    def retire_data(self, t: Task, k: TaskId) -> None:
        if t.name == self.last_data:
            self.dbg("Retiring last data: %s", self.last_data)
            self.data_in_flight.clear()
        return None

    def wait(self, page: Page) -> None:
        time_difference_s = page.created_at_s - self.parent.get_time_s()
        if time_difference_s > 0:
            time.sleep(time_difference_s)
