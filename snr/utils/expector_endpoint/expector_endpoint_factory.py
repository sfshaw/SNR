from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from ..expector_protocol import ExpectorProtocol
from . import expector_endpoint


class ExpectorEndpointFactory(EndpointFactory):
    def __init__(self,
                 expector: ExpectorProtocol[TaskId],
                 name: ComponentName = "expector",
                 exit_when_satisfied: bool = False
                 ) -> None:
        super().__init__()
        self.expector = expector
        self.endpoint_name = name
        self.exit_when_satisfied = exit_when_satisfied

    def get(self, parent: AbstractNode) -> AbstractEndpoint:
        return expector_endpoint.ExpectorEndpoint(self,
                                                  parent,
                                                  self.endpoint_name,
                                                  self.expector,
                                                  self.exit_when_satisfied)
