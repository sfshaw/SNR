""" Defines the basic unit of work for Nodes and Endpoints
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Dict, List, Tuple, Union


class TaskPriority(Enum):
    high = 3
    normal = 2
    low = 1


class TaskType(Enum):
    event = "event"
    process_data = "process_data"
    reload = "reload"
    terminate = "terminate"


TaskId = Union[TaskType, Tuple[TaskType, str]]


class Task:
    def __init__(self,
                 type: TaskType,
                 name: str,
                 priority: TaskPriority = TaskPriority.normal,  # unused
                 val_list: List[Any] = []
                 ) -> None:
        self.type = type
        self.name = name
        self.priority = priority
        self.val_list = val_list

    def id(self) -> TaskId:
        return (self.type, self.name)

    # def to_json(self) -> str:
    #     return jsons.dumps(self)

    def __eq__(self, other: Any):
        return (
            (self.__class__ == other.__class__) and
            (self.name == other.task_type) and
            (self.priority == other.priority) and
            (self.val_list == other.val_list))

    def __repr__(self):
        return "Task({}): type: {}, priority: {}, val_list: {}".format(
            self.name, self.type, self.priority, self.val_list)


def event(name: str, val_list: List[Any] = []) -> Task:
    return Task(TaskType.event, name, val_list=val_list)


def process_data(name: str) -> Task:
    return Task(TaskType.process_data, name)


def reload(endpoint_name: str) -> Task:
    return Task(TaskType.reload, endpoint_name)


def terminate(reason: str) -> Task:
    return Task(TaskType.terminate, reason)


SomeTasks = Union[None, Task, List[Task]]
TaskHandler = Callable[[Task, TaskId], SomeTasks]
TaskHandlerMap = Dict[TaskId, TaskHandler]
TaskSource = Callable[[], SomeTasks]
