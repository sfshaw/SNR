""" Defines the basic unit of work for Nodes and Endpoints
"""
import dataclasses
import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import dataclasses_json

from .page import Page
from .serializable import JsonData

# class TaskPriority(Enum):
#     high = 3
#     normal = 2
#     low = 1


class TaskType(Enum):
    event = 'event'
    '''A generic event
    '''
    store_page = 'store_page'
    '''Triggered to write a page to the datastore
    '''
    process_data = 'process_data'
    '''Triggered after a page is written to the datastore
    '''
    reload = 'reload'
    '''Triggered to cause a specific endpoint to be reloaded
    '''
    terminate = 'terminate'
    '''Triggered to terminate the node
    '''

    def __repr__(self) -> str:
        return self.value


TaskId = Union[TaskType, Tuple[TaskType, str]]


@dataclasses.dataclass
class Task(dataclasses_json.DataClassJsonMixin):
    def __init__(self,
                 type: TaskType,
                 name: str,
                 #  priority: TaskPriority = TaskPriority.normal,
                 val_list: List[Any] = []
                 ) -> None:
        self.type = type
        self.name = name
        # self.priority = priority
        self.val_list = val_list

    def id(self) -> TaskId:
        return (self.type, self.name)

    def serialize(self) -> bytes:
        return self.to_json().encode()  # type: ignore

    @classmethod
    def deserialize(cls, json: Optional[JsonData]) -> Optional['Task']:
        try:
            return cls.from_json(json)  # type: ignore
        except Exception as e:
            log = logging.getLogger('Task')
            log.error("Could not deserialize Task from json: %s, e: %s",
                      json, e)
            return None

    def __eq__(self, other: Any):
        return (
            (self.__class__ == other.__class__) and
            (self.name == other.task_type) and
            # (self.priority == other.priority) and
            (self.val_list == other.val_list))

    def __repr__(self):
        # return "Task({}): type: {}, priority: {}, val_list: {}".format(
        #     self.name, self.type, self.priority, self.val_list)
        return "Task({}): type: {}, val_list: {}".format(
            self.name, self.type,
            #  self.priority,
            self.val_list)


SomeTasks = Union[None, Task, List[Task]]
TaskHandler = Callable[[Task, TaskId], SomeTasks]
TaskHandlerMap = Dict[TaskId, TaskHandler]
TaskSource = Callable[[], SomeTasks]
TaskScheduler = Callable[[Task], None]


def task_event(name: str, val_list: List[Any] = []) -> Task:
    return Task(TaskType.event, name, val_list=val_list)


def task_store_page(page: Page) -> Task:
    return Task(TaskType.store_page, page.key, val_list=[page])


def task_process_data(name: str) -> Task:
    return Task(TaskType.process_data, name)


def task_reload(endpoint_name: str) -> Task:
    return Task(TaskType.reload, endpoint_name)


def task_terminate(reason: str) -> Task:
    return Task(TaskType.terminate, reason)
