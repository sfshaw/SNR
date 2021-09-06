from snr import *

import controller_loop


class ControllerLoopFactory(LoopFactory):

    output_data: DataKey

    def __init__(self, output_data: DataKey = "raw_controller_input") -> None:
        super().__init__([controller_loop])
        self.output_data = output_data

    def get(self,
            parent: AbstractNode,
            ) -> controller_loop.ControllerLoop:
        return controller_loop.ControllerLoop(self,
                                              parent,
                                              self.output_data)
