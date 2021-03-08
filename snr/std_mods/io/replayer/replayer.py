import time

from snr.core import *

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
                         "replayer")
        self.reader = PageReader(self, "page_reader", filename)
        self.last_data: Optional[DataKey] = None
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.next_page: Optional[Page] = None

    def setup(self) -> None:
        self.parent.store_data(f"{self.name}_pages_in_flight",
                               0,
                               process=False)

    def loop_handler(self) -> None:
        if not self.done:
            page = self.reader.read()
            if page:
                self.wait(page)
                self.parent.store_page(page)
                self.last_data = page.key
            elif not self.done:
                self.dbg("Reader Done")
                self.done = True
                if self.exit_when_done:
                    self.dbg("Reader scheduling terminate task")
                    self.parent.schedule(task_terminate("replayer_done"))

    def terminate(self) -> None:
        self.reader.close()

    def wait(self, page: Page) -> None:
        time_difference_s = page.created_at_s - self.parent.get_time_s()
        if time_difference_s > 0:
            time.sleep(time_difference_s)
