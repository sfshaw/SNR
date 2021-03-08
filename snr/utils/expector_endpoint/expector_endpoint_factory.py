from snr.core import *

from . import expector_endpoint
from ..expector_protocol import ExpectorProtocol


class ExpectorEndpointFactory(EndpointFactory):
    def __init__(self,
                 expector: ExpectorProtocol,
                 exit_when_satisfied: bool = False
                 ) -> None:
        super().__init__()
        self.expector = expector
        self.exit_when_satisfied = exit_when_satisfied

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return expector_endpoint.ExpectorEndpoint(self,
                                                  parent,
                                                  self.expector,
                                                  self.exit_when_satisfied)
