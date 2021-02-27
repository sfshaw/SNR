from snr.core.base import *

from .connection import Connection

POLL_TIMEOUT = 0.00001


class PipeLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 pipe: Connection,
                 data_keys: List[DataKey],
                 ) -> None:
        super().__init__(factory, parent, "pipe_loop")
        self.pipe = pipe
        self.task_handlers: TaskHandlerMap = {}
        for key in data_keys:
            self.task_handlers[(TaskType.process_data, key)
                               ] = self.process_data

    def process_data(self, task: Task, key: TaskId):
        page = self.parent.get_page(task.name)
        if page:
            try:
                self.pipe.send(page.serialize())
            except Exception as e:
                self.err("Error send: %s", e)
                raise e
        else:
            self.err("Data with key %s not found", task.name)

    def setup(self) -> None:
        pass

    def loop_handler(self) -> None:
        try:
            if self.pipe.poll(POLL_TIMEOUT):
                page = Page.deserialize(self.pipe.recv())
                if page:
                    self.parent.store_page(page)
                else:
                    raise Exception("Failed to deserialize Page")
            else:
                self.dbg("Did not recv anything")
        except Exception as e:
            self.err("Error recv: %s", e)
            # raise e

    def terminate(self) -> None:
        self.pipe.close()
