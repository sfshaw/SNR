from snr.core.base import *

from . import command_receiver


class CommandReceiverFactory(LoopFactory):
    def __init__(self, port: int) -> None:
        super().__init__(command_receiver)
        self.port = port

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        return command_receiver.CommandReceiver(self,
                                                parent,
                                                "command_receiver",
                                                self.port)
