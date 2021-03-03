import queue

from snr.protocol import *
from snr.types import *

from .context.context import Context, logging


class TaskQueue(Context):
    def __init__(self,
                 parent: ContextProtocol,
                 task_source: TaskSource
                 ) -> None:
        super().__init__("task_queue",
                         parent.settings,
                         parent.profiler)
        self.get_new_tasks = task_source
        self.queue: queue.Queue[Task] = queue.Queue()
        self.log.setLevel(logging.WARN)

    def schedule(self, t: SomeTasks) -> None:
        """ Adds a Task or a list of Tasks to the node's queue
        """
        if isinstance(t, Task):
            self.__schedule_task(t)
        elif t:
            # Recursively handle lists
            self.dbg("Recursively scheduling list of %s tasks",
                     len(t))
            for item in t:
                if item:
                    self.schedule(item)
        else:
            self.err("Cannot schedule %s", t)

    def __schedule_task(self, t: Task) -> None:
        # Handle normal tasks
        self.dbg("Scheduling task %s", t)
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
        next = self.queue.get()
        self.dbg("Next task: %s", next)
        self.dbg("%s tasks left in queue", self.queue.qsize())
        return next

    def is_empty(self) -> bool:
        return self.queue.empty()
