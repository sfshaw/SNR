from typing import List


class Factory:
    pass


class EndpointFactory(Factory):
    def __init__(self):
        pass

    def get(self, parent_node) -> List:
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
