import logging
from typing import Dict, List

from snr.core import *
from snr.prelude import *

POLL_TIMEOUT_MS: float = 0


class CommsLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 name: str,
                 conn: AbstractConnection,
                 data_keys: List[DataKey],
                 ) -> None:
        super().__init__(factory, parent, name)
        self.connection: AbstractConnection = conn
        self.task_handlers = self.map_handlers(data_keys)
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

    def loop(self) -> None:
        if self.connection.is_closed():
            self.err("Connection %s is closed", self.connection)
        else:
            # Pipe is open, good
            pass
        try:
            if self.connection.poll(POLL_TIMEOUT_MS):
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
                    self.parent.schedule(tasks.event(
                        tasks.REMOVE_ENDPOINT_TASK_NAME, [self.name]))
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

    def map_handlers(self,
                     data_keys: List[DataKey]
                     ) -> TaskHandlerMap:
        handlers: Dict[TaskId, TaskHandler] = {}
        for key in data_keys:
            handlers[(TaskType.process_data, key)] = self.process_data
        return handlers
