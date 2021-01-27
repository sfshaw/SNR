from queue import Queue
from typing import Callable, List, Union

from snr_core.context.context import Context
from snr_core.task import SomeTasks, Task, TaskSource

TaskScheduler = Callable[[Task], None]


class TaskQueue(Context):
    def __init__(self,
                 parent: Context,
                 task_source: TaskSource
                 ) -> None:
        super().__init__("task_queue",
                         parent,
                         parent.profiler)
        self.get_new_tasks = task_source
        self.queue: "Queue[Task]" = Queue()

    def schedule(self, t: SomeTasks) -> None:
        """ Adds a Task or a list of Tasks to the node's queue
        """
        if isinstance(t, Task):
            self.__schedule_task(t)
        elif isinstance(t, List):
            # Recursively handle lists
            self.dbg("Recursively scheduling list of {} tasks",
                     [len(t)])
            for item in t:
                self.schedule(item)
        else:
            self.err("Cannot schedule {} object {}", [type(t), t])

    def __schedule_task(self, t: Task) -> None:
        # Handle normal tasks
        self.dbg("Scheduling task {}", [t])
        # Ignore Priority
        self.queue.put(t)

    def get_next(self) -> Union[Task, None]:
        """Take the next task off the queue
        """
        if self.queue.empty():
            new_tasks = self.get_new_tasks()
            if new_tasks:
                self.schedule(new_tasks)
            else:
                return None
        return self.queue.get()

    def is_empty(self) -> bool:
        return self.queue.empty()
