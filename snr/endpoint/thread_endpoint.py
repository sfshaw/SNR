from __future__ import annotations

from threading import Event, Thread
from typing import List

from snr.endpoint.endpoint import Endpoint
from snr.factory import Factory
from snr.node import Node
from snr.task import TaskHandlerMap, TaskSource

DEFAULT_TICK_RATE = 24
JOIN_TIMEOUT = None


class ThreadEndpoint(Endpoint):
    """An Asynchronous endpoint of data for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def __init__(self,
                 factory: Factory,
                 parent: Node,
                 name: str,
                 tick_rate_hz: float = DEFAULT_TICK_RATE,
                 task_producers: List[TaskSource] = [],
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name,
                         task_producers,
                         task_handlers)
        self.parent = parent
        self.set_delay(tick_rate_hz)
        self.__terminate_flag = Event()
        self.__thread = Thread(target=self.threaded_method,
                               name=self.name + "_thread")

    def set_delay(self, tick_rate_hz: float):
        if tick_rate_hz == 0:
            self.delay_s = 0.0
        else:
            self.delay_s = 1.0 / tick_rate_hz

    def setup(self) -> None:
        pass

    def loop_handler(self) -> None:
        raise NotImplementedError

    def start(self):
        self.dbg("Starting async endpoint {} thread",
                 [self.name])
        self.__thread.start()

    def join(self):
        """Externaly wait to shutdown a threaded endpoint
        """
        self.set_terminate_flag()
        if self.__thread.is_alive():
            self.__thread.join(timeout=JOIN_TIMEOUT)
        else:
            self.warn("Thread was not alive on join")

    def threaded_method(self):
        self.setup()
        try:
            while not self.__terminate_flag.is_set():
                if self.profiler:
                    self.time(self.name, lambda _: self.loop_handler(), None)
                else:
                    self.loop_handler()
                self.tick()
        except KeyboardInterrupt:
            pass

        self.dbg("Async endpoint {} exited loop", [self.name])
        self.terminate()

    def get_name(self):
        return self.name

    def tick(self):
        if (self.delay_s == 0.0):
            self.warn("Async_endpoint {} does not sleep (max tick rate)",
                      [self.name])
        else:
            self.sleep(self.delay_s)

    def is_terminated(self) -> bool:
        return self.__terminate_flag.is_set()

    def set_terminate_flag(self) -> None:
        self.__terminate_flag.set()

    def terminate(self):
        pass
