from __future__ import annotations

from typing import Any, Callable, List

from snr_core.endpoint.endpoint_base import EndpointBase
from snr_core.factory.factory_base import FactoryBase
from snr_core.node import Node
from snr_core.task import TaskHandlerMap, TaskSource
from snr_core.utils.utils import no_op


class Endpoint(EndpointBase):
    def __init__(self,
                 factory: FactoryBase,
                 parent: Node,
                 name: str,
                 task_producers: List[TaskSource] = [],
                 task_handlers: TaskHandlerMap = {},
                 start: Callable[[], None] = no_op,
                 terminate: Callable[[], None] = no_op,
                 ) -> None:
        super().__init__(factory, parent, name,
                         start, terminate,
                         task_producers, task_handlers)
        self.parent = parent

    def start(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def reload(self, parent_node: Any) -> EndpointBase:
        self.factory.reload()
        new_endpoint = self.factory.get(parent_node)
        return new_endpoint

    def __repr__(self) -> str:
        return self.name
