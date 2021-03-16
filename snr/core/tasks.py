from typing import Any, List

from snr.interfaces import *
from snr.type_defs import *

ADD_COMPONENT_TASK_NAME: TaskName = "add_component"
REMOVE_ENDPOINT_TASK_NAME: TaskName = "remove_endpoint"


def event(name: str, val_list: List[Any] = []) -> Task:
    return Task(TaskType.event,
                name,
                val_list=val_list)


def store_page(page: Page) -> Task:
    return Task(TaskType.store_page,
                page.key,
                val_list=[page])


def process_data(key: DataKey) -> Task:
    return Task(TaskType.process_data, key)


def reload_component(name: ComponentName) -> Task:
    return Task(TaskType.reload, name)


def terminate(reason: str) -> Task:
    return Task(TaskType.terminate,
                reason,
                priority=TaskPriority.high)


def add_component(factory: AbstractFactory,
                  start_component: bool = True,
                  ) -> Task:
    return event("add_component",
                 val_list=[factory,
                           start_component])
