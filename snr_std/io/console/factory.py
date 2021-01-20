
from snr_core.endpoint.endpoint import Endpoint
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.endpoint.reloadable_factory import ReloadableEndpointFactory
from snr_core.node import Node
from snr_std.io.console import command_processor, command_receiver


class CommandReceiverFactory(EndpointFactory):
    def __init__(self, port: int) -> None:
        super().__init__("Command Receiver Factory")
        self.port = port

    def get(self, parent: Node) -> Endpoint:
        return command_receiver.CommandReceiver(self,
                                                parent,
                                                "command_receiver",
                                                self.port)


class CommandProcessorFactory(ReloadableEndpointFactory):
    def __init__(self) -> None:
        super().__init__(command_processor,
                         "command_processor_factory")

    def get(self, parent: Node) -> Endpoint:
        return command_processor.CommandProcessor(self,
                                                  parent)
