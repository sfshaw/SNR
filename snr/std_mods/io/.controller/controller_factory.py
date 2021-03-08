from snr.core import *
from snr.std_mods.io.controller import controller


class ControllerFactory(LoopFactory):
    def __init__(self, output_data_name: str):
        super().__init__("Controller Factory")
        self.output_data_name = output_data_name

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return controller.Controller(self,
                                     parent,
                                     self.output_data_name)
