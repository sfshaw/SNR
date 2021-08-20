# from abc import ABC, abstractmethod
# from typing import Optional, Tuple

# from .task import SomeTasks, Task, TaskHandler, TaskHandlerMap, TaskId


# class ProvidesTaskHandlers(ABC):

#     task_handlers: TaskHandlerMap

#     def get_task_handler(self,
#                          task: Task
#                          ) -> Optional[Tuple[TaskHandler, TaskId]]:
#         """Given a task to handle, get the matching handlers from an
# Endpoint.
#         Returns a tuple of the found handler and the key that found it,
# if any.
#         """
#         id: TaskId = (task.type, task.name)
#         handler = self.task_handlers.get(id)
#         if handler:
#             return (handler, id)

#         handler = self.task_handlers.get(task.type)
#         if handler:
#             return (handler, task.type)

#         return None


# class ProvidesTasks(ABC):

#     @abstractmethod
#     def task_source(self) -> SomeTasks:
#         ...


# class SchedulesTasks(ABC):

#     @abstractmethod
#     def schedule(self, t: SomeTasks) -> None:
#         ...
