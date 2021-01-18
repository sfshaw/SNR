from typing import Optional, TextIO

from snr_core import task
from snr_core.datastore.page import Page
from snr_core.endpoint.factory import Factory
from snr_core.endpoint.thread_endpoint import ThreadEndpoint
from snr_core.node import Node
from snr_core.utils.timer import Timer

NAME_PREFIX = "raw_replayer_"


class RawDataReplayer(ThreadEndpoint):
    def __init__(self,
                 factory: Factory,
                 parent: Node,
                 filename: str,
                 data_name: str,
                 exit_when_done: bool
                 ) -> None:
        super().__init__(factory,
                         parent,
                         NAME_PREFIX + data_name,
                         self.loop_handler)
        self.data_name = data_name
        self.filename = filename
        self.file: Optional[TextIO] = None
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.timer = Timer()
        self.next_page: Optional[Page] = None

    def setup(self) -> None:
        try:
            self.file = open(self.filename)
            pass
        except Exception as e:
            self.err("{}", [e])
            if self.exit_when_done:
                self.parent.schedule(
                    task.terminate("replayer_done"))
            self.file = None

    def loop_handler(self) -> None:
        try:
            if self.file:
                line = self.file.readline().rstrip()
                if len(line) > 0:
                    self.parent.store_data(self.data_name, line)
                else:
                    raise EOFError
            elif self.done:
                pass
            else:
                self.close()
        except EOFError:
            self.close()
        finally:
            if not self.done and not self.file:
                self.set_delay(1.0)
                self.done = True
                if self.exit_when_done:
                    self.parent.schedule(
                        task.terminate("replayer_done"))

    def close(self) -> None:
        if self.file:
            self.file.close()
            self.file = None
