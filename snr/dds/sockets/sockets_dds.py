from typing import List

from snr.context import Context
from snr.dds.dds import DDS
from snr.dds.dds_connection import DDSConnection
from snr.dds.factory import DDSFactory
from snr.dds.page import InboundStoreFn, Page
from snr.dds.sockets.client import SocketsClient
from snr.dds.sockets.config import SocketsConfig
from snr.dds.sockets.discovery_client import DiscoveryClient
from snr.dds.sockets.server import SocketsServer
from snr.node import Node

"""
DDS
-----------------------
send(), inbound_store()
-----------------------
SocketsDDS(DDS Connection)
Client - consumer thread
Server - DDS tx consumer thread
"""


class SocketsDDSFactory(DDSFactory):
    def __init__(self,
                 hosts: List[str],
                 port: int):
        super().__init__()
        self.hosts = hosts
        self.port = port

    def get(self,
            parent_node: Node,
            parent_dds: DDS
            ) -> List[DDSConnection]:
        if parent_node:
            local_ip, hosts = DiscoveryClient(
                parent_node).find_me(
                parent_node.role,
                self.hosts)
            parent_dds.inbound_store(
                Page("node_ip_address",
                     local_ip, 
                     parent_node.name,
                     parent_dds.timer.current()))
            parent_node.info("Assigned {} node ip: {}",
                             [parent_node.name, local_ip])
            return [SocketsDDS(parent_dds,
                               parent_node,
                               SocketsConfig(host, self.port),
                               parent_dds.inbound_store)
                    for host in hosts]
        else:
            return []

    def __repr__(self) -> str:
        return f"Sockets DDS Factory (hosts: {self.hosts}, port: {self.port})"


class SocketsDDS(DDSConnection):
    def __init__(self,
                 parent_context: Context,
                 parent_node: Node,
                 config: SocketsConfig,
                 inbound_store: InboundStoreFn):
        super().__init__("Sockets DDS Connection",
                         parent_context,
                         inbound_store)

        self.server = SocketsServer(self,
                                    config,
                                    inbound_store)
        self.client = SocketsClient(parent_node, config)

    def send(self, data: Page):
        self.client.send_data(data)
