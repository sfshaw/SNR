from typing import List

from ....core import *
from ....prelude import *


class PrinterEndpoint(Endpoint):

    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 keys: List[TaskId],
                 ) -> None:
        super().__init__(factory, parent, "printer_endpoint")

        self.task_handlers = {key: self.print
                              for key in keys}

    def print(self, t: Task, id: TaskId) -> None:
        print(f"{id}: {t.val_list}")

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
