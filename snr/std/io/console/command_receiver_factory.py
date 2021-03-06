from snr.core.base import *

from ...comms.sockets import sockets_listener_factory
from . import command_processor_factory, console


class CommandReceiverFactory(LoopFactory):
    def __init__(self, port: int = console.DEFAULT_PORT) -> None:
        super().__init__([command_processor_factory,
                          console,
                          sockets_listener_factory])
        self.port = port

    def get(self, parent: NodeProtocol) -> LoopProtocol:
        parent.add_component(
            command_processor_factory.CommandProcessorFactory())
        return sockets_listener_factory.SocketsListenerFactory(
            self.port,
            data_keys=[console.COMMAND_ACK_DATA_NAME],
            loop_name="command_receiver_loop",
        ).get(parent)
