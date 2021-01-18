from snr.endpoint.endpoint import Endpoint
from snr.endpoint.factory import Factory
from snr.node import Node


class EndpointFactory(Factory):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get(self, parent: Node) -> Endpoint:
        raise NotImplementedError

    def reload(self) -> None:
        # Stub for reloadable endpoints
        pass


"""Example factory that might be implemented for an endpoint
"""

# from snr.node import Node
#
# import my_endpoint
#
# class FactoryTemplate(EndpointFactory):
#     def __init__(self, stuff: str):
#         super().__init__("my_endpoint_factory")
#         self.stuff = stuff
#
#     def get(self, parent: Node) -> Endpoint:
#         return my_endpoint.MyEndpoint(self, parent, self.stuff)
