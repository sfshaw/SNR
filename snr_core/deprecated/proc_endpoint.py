from multiprocessing import Process
from typing import Any

from snr_core.endpoint.factory import FactoryBase
from snr_core.endpoint.synchronous_endpoint import Endpoint
from snr_core.node import Node

JOIN_TIMEOUT = 0.5


class ProcEndpoint(Endpoint):

    def __init__(self,
                 factory: FactoryBase,
                 parent: Node,
                 name: str,
                 tick_rate_hz: float
                 ) -> None:
        super().__init__(factory, parent, name)
        self.terminate_flag = False
        self.set_delay(tick_rate_hz)
        if parent:
            self.profiler = parent.profiler
        else:
            self.profiler = None

    def set_delay(self, tick_rate_hz: float):
        if tick_rate_hz == 0:
            self.delay = 0.0
        else:
            self.delay = 1.0 / tick_rate_hz

    def start(self):
        self.info("Starting proc endpoint {} process", [self.name])
        self.proc = self.get_proc()
        self.proc.start()

    def get_proc(self):
        return Process(target=self.threaded_method, daemon=False)

    def join(self):
        self.set_terminate_flag("join")
        self.proc.join(JOIN_TIMEOUT)

    def threaded_method(self):
        # signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            self.setup()
            while not self.terminate_flag:

                if self.profiler is None:
                    self.loop_handler()
                else:
                    self.time(self.name,
                              self.loop_handler,
                              None)

                    # self.dbg("profiling_endpoint",
                    #       "Ran {} task in {:6.3f} us",
                    #       [self.name, runtime * 1000000])
                self.tick()
        except (Exception, KeyboardInterrupt) as e:
            self.err("{}, e: {}", [self.name, str(e)])
            # self.parent.set_terminate_flag(str(e))

        self.dbg("Proc endpoint {} exited loop",
                 [self.name])
        self.terminate()
        return

    def setup(self) -> None:
        pass

    def loop_handler(self, *args: Any) -> None:
        raise NotImplementedError

    def get_name(self):
        return self.name

    def tick(self):
        if (self.delay == 0.0):
            self.warn("Proc_endpoint {} does not sleep (max tick rate)",
                      [self.name])
        else:
            self.sleep(self.delay)

    def set_terminate_flag(self, reason: str):
        self.terminate_flag = True
        self.info("Preparing to terminate proc_endpoint {} for {}",
                  [self.name, reason])

    def terminate(self) -> None:
        raise NotImplementedError
