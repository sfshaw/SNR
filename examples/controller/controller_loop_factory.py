from snr import *


class ControllerLoopFactory(LoopFactory):

    output_data: DataKey

    def __init__(self, output_data: DataKey = "raw_controller_input") -> None:
        super().__init__()
        self.output_data = output_data

    def get(self,
            parent: AbstractNode,
            ) -> ThreadLoop:
        import controller_loop
        self.reload_targets = [controller_loop]
        return controller_loop.ControllerLoop(self,
                                              parent,
                                              self.output_data)
