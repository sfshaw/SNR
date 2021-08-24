import logging
from typing import Optional

from snr.core import *
from snr.prelude import *

from .page_reader import PageReader


class ReplayerLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 filename: str,
                 exit_when_done: bool,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "replayer",
                         max_tick_rate_hz=4000)
        self.log.setLevel(logging.WARNING)
        self.reader = PageReader(self, "page_reader", filename)
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.next_page: Optional[Page] = None

    def setup(self) -> None:
        self.timer = Timer()
        self.next_page = self.reader.read()

    def loop(self) -> None:
        if not self.done:
            page = self.next_page
            while (page
                   and (self.timer.current_s() - self.delay_s >=
                        page.created_at_s)):
                self.parent.store_page(page)
                page = self.reader.read()
            if page:
                self.next_page = page
            else:
                self.dbg("Reader Done")
                self.done = True
                if self.exit_when_done:
                    self.dbg("Reader scheduling terminate task")
                    self.schedule(tasks.terminate("replayer_done"))

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        self.reader.close()
