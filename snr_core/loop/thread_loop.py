from threading import Event, Thread
from typing import Callable

from snr_core.context.context import Context
from snr_core.loop.loop_factory import LoopFactory
from snr_core.protocols import *
from snr_core.utils.utils import no_op

DEFAULT_TICK_RATE = 24
JOIN_TIMEOUT = None


class ThreadLoop(Context):
    """An Asynchronous endpoint of data for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 name: str,
                 loop_handler: Callable[[], None],
                 setup: Callable[[], None] = no_op,
                 terminate: Callable[[], None] = no_op,
                 tick_rate_hz: float = DEFAULT_TICK_RATE
                 ) -> None:
        super().__init__(name, parent)
        self.parent = parent
        self.setup = setup
        self.loop_handler = loop_handler
        self.terminate = terminate
        self.set_delay(tick_rate_hz)
        self.__terminate_flag = Event()
        self.__thread = Thread(target=self.threaded_method,
                               name=self.name + "_thread")

    def set_delay(self, tick_rate_hz: float):
        if tick_rate_hz == 0:
            self.delay_s = 0.0
        else:
            self.delay_s = 1.0 / tick_rate_hz

    def start(self):
        self.dbg("Starting %s loop thread", self.name)
        self.__thread.start()

    def join(self):
        """Externaly wait to shutdown a thread loop
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
                    self.time(self.name, self.loop_handler, [])
                else:
                    self.loop_handler()
                self.tick()
        except KeyboardInterrupt:
            pass

        self.dbg("Thread Loop %s exited loop", self.name)
        self.terminate()

    def tick(self):
        if (self.delay_s == 0.0):
            self.warn("Thread %s does not sleep (max tick rate)",
                      self.name)
        else:
            self.sleep(self.delay_s)

    def is_terminated(self) -> bool:
        return self.__terminate_flag.is_set()

    def set_terminate_flag(self) -> None:
        self.__terminate_flag.set()
