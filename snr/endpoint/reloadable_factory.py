import importlib
from importlib import reload
from typing import Any

from snr.endpoint import Endpoint
from snr.factory import Factory


class ReloadableEndpointFactory(Factory):
    def __init__(self,
                 child_module: importlib.types.ModuleType,
                 name: str) -> None:
        super().__init__(name)
        self.child_module: importlib.types.ModuleType = child_module

    def get(self, parent_node: Any) -> Endpoint:
        raise NotImplementedError

    def reload(self) -> None:
        reload(self.child_module)


"""Example factory that might be implemented for an endpoint
"""

# from snr.node import Node

# import my_endpoint

# class ReloadableFactoryTemplate(ReloadableEndointFactory):
#     def __init__(self, stuff: str):
#         super().__init__(my_endpoint, "my_factory")
#         self.stuff = stuff

#     def get(self, parent_node: Node) -> Endpoint:
#         return my_endpoint.MyEndpoint(self, parent_node, self.stuff)
