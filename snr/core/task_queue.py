import logging
import queue as que
from typing import Optional

from snr.interfaces import *
from snr.type_defs import *

from .contexts import Context


class TaskQueue(Context, AbstractTaskQueue):

    queue: que.Queue[Task]

    def __init__(self,
                 parent: AbstractContext,
                 task_source: TaskSource,
                 ) -> None:
        super().__init__("task_queue",
                         parent.profiler,
                         parent.timer)
        self.task_source = task_source
        self.queue = que.Queue()
        self.log.setLevel(logging.WARNING)

    def schedule(self, t: SomeTasks) -> None:
        """ Adds a Task or a list of Tasks to the node's queue
        """
        if isinstance(t, Task):
            self.schedule_task(t)
        elif t:
            # Recursively handle lists
            self.dbg("Recursively scheduling list of %s tasks",
                     len(t))
            for item in t:
                if item:
                    self.schedule(item)
        else:
            self.err("Cannot schedule %s", t)

    def schedule_task(self, t: Task) -> None:
        # Handle normal tasks
        self.dbg("Scheduling task %s", t)
        # Ignore Priority
        self.queue.put(t)

    def get_next(self) -> Optional[Task]:
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

    def get_new_tasks(self) -> SomeTasks:
        return self.task_source()

    def is_empty(self) -> bool:
        return self.queue.empty()
