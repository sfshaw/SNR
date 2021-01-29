from typing import Any, Callable, Dict, Optional

from snr.snr_types import *

from snr.snr_core.context.context import Context
from snr.snr_protocol import *
from snr.snr_core.utils.consumer import Consumer
from snr.snr_core.utils.timer import Timer
from snr.snr_core.utils.utils import no_op

SLEEP_TIME_S = 0.0005

DataDict = Dict[DataKey, Page]


class Datastore(Context):
    def __init__(self,
                 parent: NodeProtocol,
                 task_scheduler: Callable[[Task], None] = no_op
                 ) -> None:
        super().__init__("datastore", parent)

        self.parent = parent
        self.timer = Timer()
        self.data_dict: DataDict = {}
        self.schedule_task = task_scheduler

        self.inbound_consumer = Consumer[Page](
            parent.name + "_dds_inbound",
            self.write,
            SLEEP_TIME_S)
        self.info("Datastore initialized")

    def store(self, key: str, value: Any, process: bool = True) -> None:
        created_at = self.timer.current()
        page = Page(key, value, self.parent.name, created_at, process)
        self.store_page(page)

    def store_page(self, page: Page) -> None:
        self.inbound_store(page)

    def get_data(self, key: str) -> Optional[Any]:
        page: Any = self.get_page(key)
        if page:
            return page.data
        return None

    def get_page(self, key: str) -> Optional[Page]:
        # First flush the inbound queue so we have all data
        self.inbound_consumer.flush()
        return self.data_dict.get(key)

    def inbound_store(self, page: Page) -> None:
        self.inbound_consumer.put(page)

    def flush(self) -> None:
        self.inbound_consumer.flush

    def dump_data(self) -> None:
        for page in self.data_dict.values():
            self.dump("%s", page)

    def write(self, page: Page) -> None:
        self.data_dict[page.key] = page
        if page.process:
            t = task.process_data(page.key)
            self.schedule_task(t)

    def set_terminate_flag(self, reason: str):
        self.inbound_consumer.set_terminate_flag()
        self.info("Preparing to terminate datastore for %s", reason)

    def join(self) -> None:
        """Shutdown datastore threads
        """
        self.set_terminate_flag("join")
        self.flush()
        self.inbound_consumer.join_from(self.name)
