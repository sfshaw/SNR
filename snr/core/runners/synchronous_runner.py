import threading

from snr.prelude import *

from ..node import Node


class SynchronousRunner(AbstractRunner):

    def __init__(self,
                 role: Role,
                 config: AbstractConfig):
        self.role = role
        self.config = config

    def run(self) -> None:
        node: AbstractNode = Node(self.role, self.config)
        try:
            node.loop()  # Blocking loop
        except KeyboardInterrupt:
            if node:
                print("Interrupted by user, exiting")
                node.set_terminate_flag("Interrupted by user")
            else:
                print("Exiting before node was done being constructed")
        finally:
            if node:
                if not node.is_terminated():
                    node.set_terminate_flag("Runner clean up")
            for thread in threading.enumerate():
                if not thread.is_alive():
                    print("Zombie thread %s culled", thread.name)
