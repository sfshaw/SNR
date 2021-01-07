from typing import Any

from snr.endpoint.endpoint import Endpoint


class Factory:
    def __init__(self, name: str) -> None:
        self.name = name

    def get(self, parent_node: Any) -> Endpoint:
        raise NotImplementedError

    def reload(self) -> None:
        pass

    def __repr__(self):
        return self.name


"""Example factory that might be implemented for an endpoint
"""

# from snr.node import Node
#
# import my_endpoint
#
# class FactoryTemplate(Factory):
#     def __init__(self, stuff: str):
#         super().__init__()
#         self.stuff = stuff
#
#     def get(self, parent_node: Node) -> Endpoint:
#         return my_endpoint.MyEndpoint(self, parent_node, self.stuff)
