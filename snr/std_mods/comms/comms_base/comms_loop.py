import logging

from snr.core import *
from snr.core.endpoint.node_core_endpoint import REMOVE_ENDPOINT_TASK_NAME

POLL_TIMEOUT = 0.000001


class CommsLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 name: str,
                 conn: ConnectionProtocol,
                 data_keys: List[DataKey],
                 ) -> None:
        super().__init__(factory, parent, name)
        self.connection: ConnectionProtocol = conn
        for key in data_keys:
            self.task_handlers[(TaskType.process_data, key)
                               ] = self.process_data
        self.log.setLevel(logging.WARNING)

    def process_data(self, task: Task, key: TaskId):
        page = self.parent.get_page(task.name)
        if page:
            try:
                self.connection.send(page.serialize())
            except Exception as e:
                self.err("Error send: %s", e)
                raise e
        else:
            self.err("Data with key %s not found", task.name)

    def setup(self) -> None:
        self.connection.open()
        if self.connection.is_closed():
            self.err("Connection not open: %s", self.connection)

    def loop_handler(self) -> None:
        if self.connection.is_closed():
            self.err("Connection %s is closed", self.connection)
        else:
            # Pipe is open, good
            pass
        try:
            if self.connection.poll(POLL_TIMEOUT):
                data = self.connection.recv()
                if data:
                    page = Page.deserialize(data)
                    self.dbg("Decoded page: %s", page)
                    if page:
                        self.parent.store_page(page)
                    else:
                        raise Exception("Failed to deserialize Page")
                else:
                    self.warn("Recieved zero bytes, shutting down")
                    self.parent.schedule(task_event(
                        REMOVE_ENDPOINT_TASK_NAME, [self.name]))
                    self.set_terminate_flag()
            else:
                # self.dbg("Did not recv anything")
                pass
        except Exception as e:
            self.err("Error recv: %s", e)
            # raise e

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        self.connection.close()
