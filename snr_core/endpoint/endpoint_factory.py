from snr_core.endpoint.endpoint import EndpointBase
from snr_core.factory.factory_base import FactoryBase
from snr_core.node import Node


class EndpointFactory(FactoryBase):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get(self, parent: Node) -> EndpointBase:
        raise NotImplementedError

    def reload(self) -> None:
        # Stub for reloadable endpoints
        pass


"""Example factory that might be implemented for an endpoint
"""

# from snr import *
#
# import my_endpoint
#
# class FactoryTemplate(EndpointFactory):
#     def __init__(self, stuff: str) -> None:
#         super().__init__("my_endpoint_factory")
#         self.stuff = stuff
#
#     def get(self, parent: Node) -> Endpoint:
#         return my_endpoint.MyEndpoint(self, parent, self.stuff)
