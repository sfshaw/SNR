from snr import *
import controller_loop


class ControllerLoopFactory(LoopFactory):
    def __init__(self) -> None:
        super().__init__([controller_loop])

    def get(self,
            parent: AbstractNode,
            ) -> controller_loop.ControllerLoop:
        return controller_loop.ControllerLoop(self, parent)
