""" Defines the basic unit of work for Nodes and Endpoints
"""
import logging

from .base import *
from .page import Page


class TaskPriority(Enum):
    high = 3
    normal = 2
    low = 1


class TaskType(Enum):
    event = 'event'
    store_page = 'store_page'
    process_data = 'process_data'
    reload = 'reload'
    terminate = 'terminate'

    def __repr__(self) -> str:
        return f"TaskType.{self.value}"


TaskId = Union[TaskType, Tuple[TaskType, str]]


@dataclass
class Task(DataClassJsonMixin):
    def __init__(self,
                 type: TaskType,
                 name: str,
                 priority: TaskPriority = TaskPriority.normal,
                 val_list: List[Any] = []
                 ) -> None:
        self.type = type
        self.name = name
        self.priority = priority
        self.val_list = val_list

    def id(self) -> TaskId:
        return (self.type, self.name)

    def serialize(self) -> str:
        return self.to_json()

    @classmethod
    def deserialize(cls, json: str) -> Optional["Task"]:
        try:
            return cls.from_json(json)
        except Exception as e:
            log = logging.getLogger("Task")
            log.error("Could not deserialize Task from json: %s, e: %s",
                      json, e)
            return None

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


def store_page(page: Page) -> Task:
    return Task(TaskType.store_page, page.key, val_list=[page])


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
TaskScheduler = Callable[[Task], None]
