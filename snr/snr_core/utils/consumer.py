import logging
from queue import Empty, Queue
from threading import Event, Thread
import time
from snr.snr_types.base import *
CONSUMER_THREAD_NAME_SUFFIX = "_consumer_thread"


T = TypeVar('T')


class Consumer(Thread, Generic[T]):
    def __init__(self,
                 parent_name: str,
                 action: Callable[[T], None],
                 sleep_time: float,
                 ) -> None:
        super().__init__(target=self.__loop,
                         name=parent_name + CONSUMER_THREAD_NAME_SUFFIX)
        self.log = logging.getLogger(self.name)
        self.action = action
        self.sleep_time = sleep_time
        self.queue: "Queue[T]" = Queue()
        self.__terminate_flag = Event()
        self.flushed = Event()
        self.flushed.set()

        self.start()

    def put(self, item: T) -> None:
        if (self.is_alive() and not self.__terminate_flag.is_set()):
            self.queue.put(item)
            self.flushed.clear()
        else:
            self.log.error(
                "Consumer fed but thread is not alive ({})",
                item)

    def __loop(self) -> None:
        self.log.debug("Thread now running")
        while not self.__terminate_flag.is_set():
            self.__iterate()

            # self.fed.wait(timeout=self.sleep_time)
            time.sleep(self.sleep_time)

        # Flush remaining lines
        while not self.flushed.is_set():
            self.__iterate()
        self.flushed.set()
        self.log.debug("Thread exited loop")

    def __iterate(self) -> None:
        item: Optional[T] = None
        try:
            item = self.__get()
            if item:
                self.action(item)
        except Empty:
            pass
        except EOFError as e:
            self.log.error("EOFError: %s", e)
            self.set_terminate_flag()
        item = None
        if self.queue.empty():
            self.flushed.set()

    def __get(self) -> Optional[T]:
        return self.queue.get_nowait()

    def join_from(self, joiner: str) -> None:
        self.log.info("Preparing to join thread from %s", joiner)
        self.set_terminate_flag()
        super().join()
        if self.is_alive():
            self.log.warn("Thread just won't die.")

    def flush(self) -> None:
        if self.is_alive():
            self.flushed.wait()
        else:
            self.log.error("Cannot flush dead consumer")

    def set_terminate_flag(self) -> None:
        self.__terminate_flag.set()
