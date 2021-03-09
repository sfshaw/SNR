import threading

from snr.protocol import *
from snr.type_defs import *

from ..node import Node


class SynchronousRunner(RunnerProtocol):

    def __init__(self,
                 role: Role,
                 config: ConfigProtocol):
        self.role = role
        self.config = config

    def run(self) -> None:
        try:
            node: NodeProtocol = Node(self.role,
                                      self.config)
            node.loop()  # Blocking loop
        except KeyboardInterrupt:
            print("Interrupted by user, exiting")
        finally:
            for thread in threading.enumerate():
                if thread.is_alive() and thread != threading.main_thread():
                    print("Culling zombie thread %s", thread.name)
                    thread.join()
