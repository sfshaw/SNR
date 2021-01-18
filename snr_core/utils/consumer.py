from multiprocessing import Queue
from queue import Empty
from threading import Event, Thread
from time import sleep
from typing import Any, Callable, Generic, List, Optional, TypeVar, Union

from snr_core.utils.debug.channels import *
from snr_core.utils.utils import format_message

CONSUMER_THREAD_NAME_SUFFIX = "_consumer_thread"


T = TypeVar('T')


class Consumer(Thread, Generic[T]):
    def __init__(self,
                 parent_name: str,
                 action: Callable[[T], None],
                 sleep_time: float,
                 stdout_print: Callable[..., None] = print
                 ) -> None:
        super().__init__(target=self.__loop,
                         name=parent_name + CONSUMER_THREAD_NAME_SUFFIX)
        self.action = action
        self.sleep_time = sleep_time
        self.stdout_print = stdout_print
        self.queue: Queue[T] = Queue()
        self.__terminate_flag = Event()
        self.flushed = Event()
        self.flushed.set()

        self.start()

    def put(self, item: T) -> None:
        if (self.is_alive() and not self.__terminate_flag.is_set()):
            self.queue.put(item)
            self.flushed.clear()
        else:
            self.dbg(ERROR_CHANNEL,
                     "Consumer fed but thread is not alive ({})",
                     [item])

    def __loop(self) -> None:
        self.dbg(DEBUG_CHANNEL, "Thread now running")
        while not self.__terminate_flag.is_set():
            self.__iterate()

            # self.fed.wait(timeout=self.sleep_time)
            sleep(self.sleep_time)

        # Flush remaining lines
        while not self.flushed.is_set():
            self.__iterate()
        self.flushed.set()
        self.dbg(DEBUG_CHANNEL, "Thread exited loop")

    def __iterate(self) -> None:
        item: Optional[T] = None
        try:
            item = self.__get()
            if item:
                self.action(item)
        except Empty:
            pass
        except EOFError as e:
            msg = f"EOFError: {e}"
            self.dbg(ERROR_CHANNEL, msg)
            self.set_terminate_flag()
        item = None
        if self.queue.empty():
            self.flushed.set()

    def __get(self) -> Optional[T]:
        return self.queue.get_nowait()

    def join_from(self, joiner: str):
        self.dbg(INFO_CHANNEL, "Preparing to join thread from {}", [joiner])
        self.set_terminate_flag()
        super().join()
        if self.is_alive():
            self.dbg(WARNING_CHANNEL, "Thread just won't die.")

    def flush(self) -> None:
        if self.is_alive():
            self.flushed.wait()
        else:
            self.dbg(ERROR_CHANNEL, "Cannot flush dead consumer")

    def set_terminate_flag(self):
        self.__terminate_flag.set()

    def dbg(self,
            level: str,
            message: str,
            format_args: Union[List[Any], None] = None) -> None:
        self.stdout_print(format_message(self.name,
                                         level,
                                         message,
                                         format_args))
