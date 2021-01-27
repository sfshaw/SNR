from snr_core.base import *
from snr_core.protocol.loop_protocol import LoopProtocol
from snr_core.protocol.node_protocol import NodeProtocol
from snr_std.io.console import command_processor, command_receiver


class CommandReceiverFactory(LoopFactory):
    def __init__(self, port: int) -> None:
        super().__init__("Command Receiver Factory")
        self.port = port

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return command_receiver.CommandReceiver(self,
                                                parent,
                                                "command_receiver",
                                                self.port)


class CommandProcessorFactory(EndpointFactory):
    def __init__(self) -> None:
        super().__init__(command_processor,
                         "command_processor_factory")

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return command_processor.CommandProcessor(self,
                                                  parent)
