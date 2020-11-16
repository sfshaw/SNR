""" SNR framework for scheduling and task management

Node: Task queue driven host for data and endpoints
AsyncEndpoint: Generate and process data for Nodes
Relay: Server data to other nodes
"""

from snr.endpoint.factory import EndpointFactory
from threading import Thread
from typing import Dict, List

from snr.endpoint.endpoint import Endpoint
from snr.node import Node
from snr.task import TaskHandler, TaskSource

DEFAULT_TICK_RATE = 24
DAEMON_THREADS = False


class ThreadEndpoint(Endpoint):
    """An Asynchronous endpoint of data for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def __init__(self,
                 factory: EndpointFactory,
                 parent: Node,
                 name: str,
                 tick_rate_hz: float = DEFAULT_TICK_RATE,
                 task_producers: List[TaskSource] = [],
                 task_handlers: Dict[str, TaskHandler] = {}
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name,
                         task_producers,
                         task_handlers)
        self.parent = parent
        self.terminate_flag = False
        self.set_delay(tick_rate_hz)

        self.thread = Thread(target=self.threaded_method,
                             args=[],
                             name=f"thread_{self.name}",
                             daemon=DAEMON_THREADS)

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
        self.thread.start()

    def join(self):
        """Externaly wait to shutdown a threaded endpoint
        """
        self.set_terminate_flag("join")
        if self.thread.is_alive():
            self.thread.join(timeout=1)
        else:
            self.warn("Thread was not alive on join")

    def threaded_method(self):
        self.setup()
        try:
            while not self.terminate_flag:
                if self.profiler:
                    self.time(self.name, self.loop_handler, None)
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
        # TODO: Ensure that this does not block other threads: thread.sleep()?
        if (self.delay_s == 0.0):
            self.warn("Async_endpoint {} does not sleep (max tick rate)",
                      [self.name])
        else:
            self.sleep(self.delay_s)

    def set_terminate_flag(self, reason: str):
        self.terminate_flag = True
        self.info("Preparing to terminating async_endpoint {} for {}",
                  [self.name, reason])

    def terminate(self):
        pass
