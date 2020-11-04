from typing import Any, List

from snr.factory import Factory

from snr.endpoint.endpoint import Endpoint


class EndpointFactory(Factory):
    def __init__(self):
        pass

    def get(self, parent_node: Any) -> List[Endpoint]:
        return self.get_endpoints(parent_node)

    def get_endpoints(self, parent_node: Any = None) -> List[Endpoint]:
        raise NotImplementedError


"""Example factory that might be implemented for an endpoint
"""
# class FactoryTemplate(Factory):
#     def __init__(self, stuff: str):
#         super().__init__()
#         self.stuff = stuff

#     def get(self
#             ...
#             ) -> List[Endpoint]:
#         return [Endpoint(stuff)]
