import socket
from typing import List, Tuple

from ....core import *
from ....prelude import *
from ..sockets_base.sockets_wrapper import SocketsWrapper


class SocketsClientEndpoint(Endpoint):

    server_tuple: Tuple[str, int]

    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 server_tuple: Tuple[str, int],
                 keys: List[DataKey],
                 ) -> None:
        super().__init__(factory, parent, "sockets_client")
        self.task_handlers = {
            (TaskType.store_page, key): self.send_data
            for key in keys
        }
        self.server_tuple = server_tuple
        self.connection = SocketsWrapper(
            (socket.create_connection(self.server_tuple),
             self.server_tuple),
            self)
        self.connection.open()

    def send_data(self, task: Task, id: TaskId) -> None:
        page = task.val_list[0]
        assert isinstance(page, Page)
        self.connection.send(page.serialize())

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        self.connection.close()

    def terminate(self) -> None:
        pass
