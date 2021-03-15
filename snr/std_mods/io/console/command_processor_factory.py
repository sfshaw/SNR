from snr.core import *
from snr.interfaces import *

from . import command_processor


class CommandProcessorFactory(EndpointFactory):
    def __init__(self) -> None:
        super().__init__(command_processor)

    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        return command_processor.CommandProcessor(self,
                                                  parent)
