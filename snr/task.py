""" Defines the basic unit of work for Nodes
"""

from enum import Enum
from typing import Callable, List, Union


class TaskPriority(Enum):
    high = 3
    normal = 2
    low = 1


class Task:
    """The task class and associated code for using and passing tasks

    The Task object is one that defines a action or event on the robot
    raspberry pi or the surface unit raspberry pi
    """

    def __init__(self, task_type: str,
                 priority: TaskPriority = TaskPriority.normal,
                 val_list: List = []):
        self.task_type = task_type
        self.priority = priority
        self.val_list = val_list

    def __eq__(self, other):
        return (
            (self.__class__ == other.__class__) and
            (self.task_type == other.task_type) and
            (self.priority == other.priority) and
            (self.val_list == other.val_list)
        )

    def __repr__(self):
        return "Task: type: {}, priority: {}, val_list: {}".format(
            self.task_type, self.priority, self.val_list)


SomeTasks = Union[None, Task, List[Task]]
TaskHandler = Callable[[Task], SomeTasks]
TaskSource = Callable[[], SomeTasks]
