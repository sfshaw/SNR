from snr.endpoint.endpoint import Endpoint
from snr.node import Node


class DummyEndpoint(Endpoint):
    def __init__(self, parent_node: Node):
        super().__init__(None, "dummy_endpoint")
