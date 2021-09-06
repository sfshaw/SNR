""" Defines the basic unit of work for Nodes and Endpoints
"""
import dataclasses
import logging
from enum import Enum
from typing import Any, Callable, List, Mapping, Optional, Tuple, Union

import dataclasses_json

from .serializable import JsonData
from .page import Page


class TaskPriority(Enum):
    high = 1
    normal = 2


TaskName = str


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


TaskId = Union[TaskType, Tuple[TaskType, TaskName]]


@dataclasses.dataclass
class Task(dataclasses_json.DataClassJsonMixin):
    type: TaskType
    name: TaskName
    val_list: List[Any] = dataclasses.field(default_factory=list)

    def id(self) -> TaskId:
        return (self.type, self.name)

    def serialize(self) -> bytes:
        return self.to_json().encode()  # type: ignore

    @classmethod
    def deserialize(cls,
                    json: Optional[JsonData],
                    ) -> Optional['Task']:
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
        return "Task({}): type: {}, val_list: {}".format(
            self.name, self.type, self.val_list)

    @staticmethod
    def store_page(page: Page) -> 'Task':
        return Task(TaskType.store_page,
                    page.key,
                    val_list=[page])


SomeTasks = Union[None, Task, List[Task]]
TaskHandler = Callable[[Task, TaskId], SomeTasks]
TaskHandlerMap = Mapping[TaskId, TaskHandler]
TaskSource = Callable[[], List[Task]]
TaskScheduler = Callable[[Task], None]
