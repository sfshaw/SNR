from typing import Optional

from snr_core import task
from snr_core.datastore.page import Page
from snr_core.loop.loop_factory import LoopFactory
from snr_core.loop.thread_loop import ThreadLoop
from snr_core.node import Node
from snr_core.utils.timer import Timer


class Replayer(ThreadLoop):

    def __init__(self,
                 factory: LoopFactory,
                 parent: Node,
                 filename: str,
                 exit_when_done: bool
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "replayer",
                         self.loop_handler)
        self.file = open(filename)
        self.exit_when_done = exit_when_done
        self.timer = Timer()
        self.next_page: Optional[Page] = None

    def loop_handler(self) -> None:
        if (self.prepare_page() and self.next_page):
            self.handle_page(self.next_page)
        else:
            self.set_terminate_flag()
            if self.exit_when_done:
                self.parent.schedule(
                    task.terminate("replayer_done"))

    def prepare_page(self) -> bool:
        if not self.next_page:
            return self.read_page()
        return True

    def terminate(self) -> None:
        if self.file:
            self.file.close()
            self.file = None

    def handle_page(self, page: Page) -> None:
        if self.is_ready():
            self.store_page()
        else:
            self.set_sleep()

    def set_sleep(self) -> None:
        if isinstance(self.next_page, Page):
            time_to_sleep = self.next_page.created_at - self.timer.current()
            self.set_delay(1.0/time_to_sleep)
        else:
            raise Exception("Cannot sleep on non-Page data")

    def read_page(self) -> bool:
        self.next_page = None   # todo: read file
        return self.next_page is not None

    def store_page(self) -> None:
        if isinstance(self.next_page, Page):
            self.parent.store_data(self.next_page.key,
                                   self.next_page.data)
            self.next_page = None
        else:
            raise Exception("Cannot store non-Page data")

    def is_ready(self) -> bool:
        if isinstance(self.next_page, Page):
            return self.next_page.created_at < self.timer.current()
        else:
            raise Exception("Not ready, non-Page data read")
