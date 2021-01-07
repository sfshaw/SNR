
from typing import Any, Callable, Dict, Optional

from snr.context.context import Context
from snr.dds.page import Page
from snr.task import PROCESS_DATA_PREFIX, Task
from snr.utils.consumer import Consumer
from snr.utils.timer import Timer
from snr.utils.utils import no_op

SLEEP_TIME = 0.001
JOIN_TIMEOUT = 0.5
DAEMON_THREADS = False

DataDict = Dict[str, Page]


class DDS(Context):
    def __init__(self,
                 parent_node: Any,
                 task_scheduler: Callable[[Task], None] = no_op
                 ) -> None:
        super().__init__("dds", parent_node)

        self.parent_node = parent_node
        self.timer = Timer()
        self.data_dict: DataDict = {}
        self.schedule_task = task_scheduler

        self.inbound_consumer = Consumer[Page]("dds_inbound",
                                               self.write,
                                               SLEEP_TIME,
                                               self.stdout.print)
        self.info("DDS initialized")

    def store(self, key: str, value: Any, process: bool = True) -> None:
        created_at = self.timer.current()
        page = Page(key, value, self.parent_node.name, created_at, process)
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
            super().dump("{}", [page])

    def write(self, page: Page):
        self.data_dict[page.key] = page
        if page.process:
            self.schedule_task(Task(f"{PROCESS_DATA_PREFIX}{page.key}"))

    def set_terminate_flag(self, reason: str):
        self.inbound_consumer.set_terminate_flag(reason)
        self.info("Preparing to terminate DDS for {}", [reason])

    def join(self):
        """Shutdown DDS threads
        """
        self.set_terminate_flag("join")
        self.flush()
        self.inbound_consumer.join_from(self.name)
