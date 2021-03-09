from snr.core import *
from snr.protocol import *

from . import command_processor


class CommandProcessorFactory(EndpointFactory):
    def __init__(self) -> None:
        super().__init__(command_processor)

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return command_processor.CommandProcessor(self,
                                                  parent)
