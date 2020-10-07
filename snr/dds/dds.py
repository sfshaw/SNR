from queue import Empty
from snr.dds.factory import DDSFactory
from threading import Thread
from time import sleep, time
from typing import Callable, Dict, List

# Injection of Queue type
from multiprocessing import Queue as Queue

from snr.dds.dds_connection import DDSConnection
from snr.dds.page import Page
from snr.context import Context
from snr.utils.consumer import Consumer
from snr.task import Task, TaskPriority
from snr.utils.utils import no_op, get_all

SLEEP_TIME = 0.001
JOIN_TIMEOUT = 0.5
DAEMON_THREADS = False


class DDS(Context):
    def __init__(self,
                 parent_context: Context,
                 parent_node=None,
                 factories: List[DDSFactory] = [],
                 task_scheduler: Callable[[Task], None] = no_op):
        super().__init__("dds", parent_context)

        self.data_dict: Dict[str, Page] = {}
        # self.inbound_que: Queue[Page] = Queue()
        # self.outbound_que: Queue[Page] = Queue()

        self.info("Creating connections from {} factories: {}",
                  [len(factories), factories])
        self.connections: List[DDSConnection] = get_all(
            factories, parent_node, self)
        self.schedule_task = task_scheduler
        # self.terminate_flag = False

        self.rx_consumer = Consumer("dds_rx", self.write, SLEEP_TIME)
        # self.rx_consumer = Thread(target=lambda:
        #                           self.__consumer(q=self.inbound_que,
        #                                           action=self.__write,
        #                                           sleep_time=SLEEP_TIME),
        #                           daemon=DAEMON_THREADS)
        self.tx_consumer = Consumer("dds_tx", self.send, SLEEP_TIME)
        # self.tx_consumer = Thread(target=lambda:
        #                           self.__consumer(q=self.outbound_que,
        #                                           action=self.send,
        #                                           sleep_time=SLEEP_TIME),
        #                           daemon=DAEMON_THREADS)

        # self.rx_consumer.start()
        # self.tx_consumer.start()

        self.info("Initialized with {} connections",
                  [len(self.connections)])

    def store(self, key: str, value):
        self.inbound_store(Page(key, value))
        self.tx_consumer.put(Page(key, value))

    def get(self, key: str):
        # if not self.inbound_que.empty():
        #     # Hope that queue gets emptied
        #     # TODO: correctly flush datastore queue
        #     sleep(4 * SLEEP_TIME)
        self.rx_consumer.catch_up()
        page = self.data_dict.get(key)
        if page:
            return page.data
        return None

    def inbound_store(self, page: Page):
        self.rx_consumer.put(page)

    def catch_up(self):
        # MAX_TIME_WAITED = 5 * SLEEP_TIME
        time_waited = time()
        # while (time_waited < MAX_TIME_WAITED
        #        and (self.inbound_que.empty
        #             or self.outbound_que.empty)):
        #     sleep(SLEEP_TIME)
        #     time_waited += SLEEP_TIME
        self.rx_consumer.catch_up()
        self.tx_consumer.catch_up()
        time_waited -= time()
        self.info("Waited {} seconds for DDS to catch up", [time_waited])

    def dump(self):
        for k in self.data_dict.keys():
            super().dump("k: {}\tv: {}",
                         [k, self.data_dict.get(k).data])

    def write(self, page: Page):
        self.data_dict[page.key] = page
        self.schedule_task(Task(f"process_{page.key}"))

    def send(self, page: Page):
        for connection in self.connections:
            try:
                connection.send(page)
            except Exception as _e:
                pass

    # def __consumer(self, q: Queue, action: Callable, sleep_time: float):
    #     """A method to be run by a thread for consuming the contents of a
    #     queue asynchronously
    #     """
    #     # Loop
    #     while not self.terminate_flag:
    #         try:
    #             page = q.get_nowait()
    #             if page is not None:
    #                 action(page)
    #                 page = q.get_nowait()
    #         except Empty:
    #             pass
    #         sleep(sleep_time)

    #     # Remaining lines
    #     try:
    #         page = q.get_nowait()
    #         while page is not None:
    #             action(page)
    #             page = q.get()
    #     except Exception as e:
    #         print(f"{e}")
    #     return

    def set_terminate_flag(self, reason: str):
        # self.terminate_flag = True
        self.rx_consumer.set_terminate_flag(reason)
        self.tx_consumer.set_terminate_flag(reason)
        self.info("Preparing to terminate DDS for {}", [reason])

    def join(self):
        """Shutdown DDS threads
        """
        self.set_terminate_flag("join")
        self.catch_up()
        # self.rx_consumer.join(JOIN_TIMEOUT)
        # self.tx_consumer.join(JOIN_TIMEOUT)
        self.rx_consumer.join()
        self.tx_consumer.join()
