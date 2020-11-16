from typing import Any, List

from snr.endpoint.endpoint import Endpoint
from snr.factory import Factory


class EndpointFactory(Factory):
    def __init__(self):
        pass

    def get(self, parent_node: Any) -> List[Endpoint]:
        return raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError


"""Example factory that might be implemented for an endpoint
"""
# from importlib import reload
#
# from snr.node import Node
#
# import my_endpoint
#
# class FactoryTemplate(Factory):
#     def __init__(self, stuff: str):
#         super().__init__()
#         self.stuff = stuff
#
#     def get(self,
#             parent_node: Node
#             ) -> List[Endpoint]:
#         return [my_endpoint.MyEndpoint(self, parent_node, stuff)]
#
#     def reload(self) -> None:
#         reload(my_endpoint)
#
#     def __repr__(self) -> str:
#         return "TemplateFactory"
