from multiprocessing import Queue
from queue import Empty
from threading import Event, Thread
from time import sleep
from typing import Any, Callable, Generic, List, Optional, TypeVar, Union

from snr.utils.debug.channels import *
from snr.utils.utils import format_message

CONSUMER_THREAD_NAME_SUFFIX = "_consumer_thread"


T = TypeVar('T')


class Consumer(Thread, Generic[T]):
    def __init__(self,
                 parent_name: str,
                 action: Callable[[T], None],
                 sleep_time: float,
                 stdout_print: Callable[..., None] = print
                 ) -> None:
        Thread.__init__(self,
                        target=self.__loop,
                        name=parent_name + CONSUMER_THREAD_NAME_SUFFIX)
        # self.name = parent_name + CONSUMER_NAME_SUFFIX
        self.action = action
        self.sleep_time = sleep_time
        self.stdout_print = stdout_print
        self.queue: Queue[T] = Queue()
        self.terminate_flag = Event()
        self.fed = Event()
        self.flushed = Event()
        self.flushed.set()

        self.start()

    def put(self, item: T) -> None:
        self.__check_alive(f"Consumer fed but thread is not alive ({item})")
        self.queue.put(item)
        self.fed.set()
        self.flushed.clear()

    def __loop(self) -> None:
        self.dbg(DEBUG_CHANNEL, "Thread now running")
        while not self.terminate_flag.is_set():
            self.__iterate()

            # self.fed.wait(timeout=self.sleep_time)
            sleep(self.sleep_time)

        # Flush remaining lines
        while not self.queue.empty():
            self.__iterate()
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
            self.set_terminate_flag(msg)
        item = None
        if self.queue.empty():
            self.fed.clear()
        if self.queue.empty():
            self.flushed.set()

    def __get(self) -> Optional[T]:
        return self.queue.get_nowait()

    def join_from(self, joiner: str, timeout: Optional[float] = None):
        self.dbg(INFO_CHANNEL, "Preparing to join thread from {}", [joiner])
        self.set_terminate_flag("join")
        self.flush()
        super().join(timeout)
        if self.is_alive():
            self.dbg(WARNING_CHANNEL, "Thread just won't die.")

    def flush(self) -> None:
        self.__check_alive("Cannot flush dead consumer")
        self.flushed.wait()

    def set_terminate_flag(self, reason: str) -> None:
        self.terminate_flag.set()

    def __check_alive(self, message: str) -> None:
        if not self.is_alive():
            self.dbg(DEBUG_CHANNEL, message, [self.name])

    def dbg(self,
            level: str,
            message: str,
            format_args: Union[List[Any], None] = None) -> None:
        self.stdout_print(format_message(self.name,
                                         level,
                                         message,
                                         format_args))
