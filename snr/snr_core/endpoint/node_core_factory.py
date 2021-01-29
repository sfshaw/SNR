from snr.snr_core.endpoint import node_core_endpoint
from snr.snr_core.endpoint.endpoint_factory import EndpointFactory
from snr.snr_protocol.endpoint_protocol import EndpointProtocol
from snr.snr_protocol.node_protocol import NodeProtocol


class NodeCoreFactory(EndpointFactory):
    def __init__(self) -> None:
        super().__init__(node_core_endpoint, "Node Core Factory")

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return node_core_endpoint.NodeCore(self, parent)
