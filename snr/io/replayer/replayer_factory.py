from snr.endpoint import Endpoint
from snr.endpoint.endpoint_factory import EndpointFactory
from snr.io.replayer import replayer
from snr.node import Node


class ReplayerFactory(EndpointFactory):
    def __init__(self,
                 input_filename: str,
                 exit: bool = False
                 ) -> None:
        super().__init__("Replayer Factory")
        self.input_filename = input_filename
        self.exit = exit

    def get(self, parent: Node) -> Endpoint:
        return replayer.Replayer(self,
                                 parent,
                                 self.input_filename,
                                 self.exit)
