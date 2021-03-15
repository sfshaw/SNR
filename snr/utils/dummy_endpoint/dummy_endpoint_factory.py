from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from . import dummy_endpoint

DEFAULT_NAME = "dummy_endpoint"


class DummyEndpointFactory(EndpointFactory):
    def __init__(self,
                 name: str = DEFAULT_NAME,
                 task_handlers: TaskHandlerMap = {}
                 ) -> None:
        super().__init__(dummy_endpoint)
        self.endpoint_name = name
        self.task_handlers = task_handlers

    def get(self, parent: AbstractNode) -> Endpoint:
        return dummy_endpoint.DummyEndpoint(self,
                                            parent,
                                            self.endpoint_name,
                                            self.task_handlers)
