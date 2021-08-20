from typing import Any, List

from snr.prelude import *

ADD_COMPONENT_TASK_NAME: TaskName = "add_component"
REMOVE_ENDPOINT_TASK_NAME: TaskName = "remove_endpoint"


def event(name: str, val_list: List[Any] = []) -> Task:
    return Task(TaskType.event,
                name,
                val_list=val_list)


def store_data(key: DataKey, data: Any, process: bool = True) -> Task:
    return Task(TaskType.store_data,
                key,
                val_list=[data, process])


def reload_component(name: ComponentName) -> Task:
    return Task(TaskType.reload, name)


def terminate(reason: str) -> Task:
    return Task(TaskType.terminate, reason)


def add_component(factory: AbstractFactory[Any],
                  start_component: bool = True,
                  ) -> Task:
    return event("add_component",
                 val_list=[factory,
                           start_component])
