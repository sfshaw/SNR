from abc import ABC
import logging
import threading
import time

from snr.interfaces import *
from snr.type_defs import *

from ..contexts import Context
from .loop_factory import LoopFactory

DEFAULT_TICK_RATE = 1000


class ThreadLoop(Context, AbstractLoop, ABC):
    """An Asynchronous endpoint of data for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).

    Concrete subclasses should implement the remaining AbstractLoop methods:
    setup(), loop_handler(), and terminate()
    """

    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 name: str,
                 max_tick_rate_hz: float = DEFAULT_TICK_RATE,
                 ) -> None:
        super().__init__(name,
                         parent.settings,
                         parent.profiler,
                         parent.timer)
        self.log.setLevel(logging.WARNING)
        self.factory = factory
        self.task_handlers: TaskHandlerMap = {}
        self.parent = parent
        self.delay_s: float = 0.0
        self.set_delay(max_tick_rate_hz)
        self.__terminate_flag = threading.Event()
        self.__thread = threading.Thread(target=self.threaded_method,
                                         name=self.name + "_thread")

    def task_source(self) -> SomeTasks:
        return None

    def set_delay(self, max_tick_rate_hz: float):
        if max_tick_rate_hz == 0:
            self.delay_s = 0.0
        else:
            self.delay_s = 1.0 / max_tick_rate_hz

    def begin(self):
        self.dbg("Starting %s loop thread", self.name)
        if not self.__thread.is_alive():
            self.__thread.start()
        else:
            self.err("Thread already running when starting Threadloop")

    def join(self):
        """Externaly wait to shutdown a thread loop
        """
        self.set_terminate_flag()
        if self.__thread.is_alive():
            self.__thread.join()
        else:
            self.warn("Thread was not alive on join")

    def threaded_method(self):
        '''Concrete implementation of ThreadLoop's loop.
        Calls user defined Loop Protocol methods setup(), loop(), and halt()
        '''
        self.setup()
        try:
            while not self.__terminate_flag.is_set():
                self.profile(self.name, self.loop)
                self.tick()
        except KeyboardInterrupt:
            pass

        self.dbg("Thread Loop %s exited loop", self.name)
        self.halt()

    def tick(self):
        if (self.delay_s == 0.0):
            self.warn("Thread %s does not sleep (max tick rate)",
                      self.name)
        else:
            time.sleep(self.delay_s)

    def is_terminated(self) -> bool:
        return self.__terminate_flag.is_set()

    def set_terminate_flag(self) -> None:
        self.__terminate_flag.set()

    def schedule(self, t: SomeTasks) -> None:
        self.parent.schedule(t)

    def store_page(self, page: Page) -> None:
        self.parent.store_page(page)
