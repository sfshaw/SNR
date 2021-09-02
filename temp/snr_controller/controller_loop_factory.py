import snr
import controller_loop


class ControllerLoopFactory(snr.LoopFactory):
    def __init__(self) -> None:
        super().__init__([controller_loop])

    def get(self,
            parent: snr.Node,
            ) -> controller_loop.ControllerLoop:
        return controller_loop.ControllerLoop(self, parent)
