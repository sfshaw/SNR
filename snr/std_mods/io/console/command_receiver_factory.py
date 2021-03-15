from snr.core import *
from snr.interfaces import *

from ...comms.sockets_comms import sockets_listener_factory
from . import command_processor_factory, remote_console


class CommandReceiverFactory(LoopFactory):
    def __init__(self, port: int = remote_console.DEFAULT_PORT) -> None:
        super().__init__([command_processor_factory,
                          remote_console,
                          sockets_listener_factory])
        self.port = port

    def get(self, parent: AbstractNode) -> AbstractLoop:
        parent.schedule(tasks.add_component(
            command_processor_factory.CommandProcessorFactory()))
        return sockets_listener_factory.SocketsListenerFactory(
            self.port,
            data_keys=[remote_console.COMMAND_ACK_DATA_NAME],
            loop_name="command_receiver_loop",
        ).get(parent)
