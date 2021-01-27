from __future__ import annotations

from typing import List

from snr_core.context.context import Context
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.endpoint.endpoint_protocol import EndpointProtocol
from snr_core.node import Node
from snr_core.task import TaskHandlerMap, TaskSource


class Endpoint(Context, EndpointProtocol):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: Node,
                 name: str,
                 task_producers: List[TaskSource] = [],
                 task_handlers: TaskHandlerMap = {},
                 ) -> None:
        super().__init__(name, parent)
        self.factory = factory
        self.parent = parent
        self.task_producers = task_producers
        self.task_handlers = task_handlers

    def reload(self, parent: Node) -> EndpointProtocol:
        self.factory.reload()
        new_endpoint = self.factory.get(parent)
        return new_endpoint

    def __repr__(self) -> str:
        return self.name
