from typing import List

from ....core import *
from ....prelude import *
from . import printer_endpoint


class PrinterEndpointFactory(EndpointFactory):

    keys: List[TaskId]

    def __init__(self, keys: List[TaskId]) -> None:
        super().__init__(printer_endpoint)
        self.keys = keys

    def get(self, parent: AbstractNode) -> Endpoint:
        return printer_endpoint.PrinterEndpoint(self,
                                                parent,
                                                self.keys)
