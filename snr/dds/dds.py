
from time import time
from typing import Any, Callable, Dict, List, Optional

from snr.context import Context
from snr.dds.dds_connection import DDSConnection
from snr.dds.factory import DDSFactory
from snr.dds.page import Page
from snr.dds.time_provider import TimeProvider
from snr.task import Task
from snr.utils.consumer import Consumer
from snr.utils.utils import get_all, no_op

SLEEP_TIME = 0.001
JOIN_TIMEOUT = 0.5
DAEMON_THREADS = False

DataDict = Dict[str, Page]


class DDS(Context):
    def __init__(self,
                 parent_node: Any,
                 factories: List[DDSFactory] = [],
                 task_scheduler: Callable[[Task], None] = no_op):
        super().__init__("dds", parent_node)

        self.timer = TimeProvider()
        self.data_dict: DataDict = {}

        self.info("Creating connections from {} factories: {}",
                  [len(factories), factories])
        self.connections: List[DDSConnection] = get_all(factories,
                                                        parent_node,
                                                        self)
        self.schedule_task = task_scheduler

        self.rx_consumer = Consumer("dds_rx", self.write, SLEEP_TIME)
        self.tx_consumer = Consumer("dds_tx", self.send, SLEEP_TIME)

        self.info("Initialized with {} connections",
                  [len(self.connections)])

    def store(self, key: str, value: Any, process: bool = True) -> None:
        created_at = self.timer.current()
        page = Page(key, value, self.parent_name, created_at, process)
        self.inbound_store(page)
        self.tx_consumer.put(page)

    def get(self, key: str) -> Optional[Any]:
        # First flush the inbound queue so we have all data
        self.rx_consumer.catch_up()
        page: Any = self.data_dict.get(key)
        if page:
            return page.data
        return None

    def inbound_store(self, page: Page) -> None:
        self.rx_consumer.put(page)

    def catch_up(self) -> None:
        time_waited = time()
        self.rx_consumer.catch_up()
        self.tx_consumer.catch_up()
        time_waited -= time()
        self.info("Waited {} ms for DDS to catch up", [time_waited * 1000])

    def dump_data(self) -> None:
        for (k, v) in self.data_dict.items():
            super().dump("k: {}\tv: {}",
                         [k, v])

    def write(self, page: Page):
        self.data_dict[page.key] = page
        if page.process:
            self.schedule_task(Task(f"process_{page.key}"))

    def send(self, page: Page):
        for connection in self.connections:
            try:
                connection.send(page)
            except Exception:
                pass

    def set_terminate_flag(self, reason: str):
        self.rx_consumer.set_terminate_flag(reason)
        self.tx_consumer.set_terminate_flag(reason)
        self.info("Preparing to terminate DDS for {}", [reason])

    def join(self):
        """Shutdown DDS threads
        """
        self.set_terminate_flag("join")
        self.catch_up()
        for connection in self.connections:
            connection.join()
        self.rx_consumer.join()
        self.tx_consumer.join()
