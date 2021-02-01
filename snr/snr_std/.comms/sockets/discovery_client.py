import socket

from snr.snr_core.base import *

from .discovery_server import DiscoveryServer

TIMEOUT = 2


class DiscoveryClient(Context):
    def __init__(self, parent_context: Context):
        super().__init__("discovery_client", parent_context)

    def find_me(self,
                local_role: str,
                hosts: List[str]
                ) -> Tuple[str, List[str]]:

        self.info("Discovering local node ip from %s", hosts)

        discovery_server = DiscoveryServer(self,
                                           local_role,
                                           self.settings.DISCOVERY_SERVER_PORT)

        local_host = None

        for host in hosts:
            self.dbg("Checking host '{}'", [host])
            node_name = self.ping((host, discovery_server.port))
            if node_name == local_role:
                self.info("Identified self as '%s'", host)
                local_host = host
                break

        discovery_server.terminate()
        self.info("Discovered self to be '%s', removeing from hosts: %s",
                  local_host, hosts)
        if local_host:
            hosts.remove(local_host)
        else:
            local_host = "localhost"
        return (local_host, hosts)

    def ping(self, target_host_tuple: Tuple[str, int]) -> str:
        """Blocking call to discovery an SNR Node running on a host.
        Returns a node name if the node discovery server responds,
        or None on timeout or error
        """
        data: str = ""
        try:
            s = socket.create_connection(target_host_tuple,
                                         self.settings.SOCKETS_CLIENT_TIMEOUT)
            # Reuse port prior to slow kernel release
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            data = s.recv(self.settings.MAX_SOCKET_SIZE).decode()
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            s = None
        except (Exception, socket.timeout) as e:
            self.warn("Did not find node at {}:{}: {}",
                      [target_host_tuple[0], target_host_tuple[1], e])
            data = ""
        return data
