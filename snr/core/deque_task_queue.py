import logging
from collections import deque
from typing import Optional

from snr.prelude import *

from .contexts import Context


class DequeTaskQueue(Context, AbstractTaskQueue):

    def __init__(self,
                 parent: AbstractContext,
                 task_source: TaskSource,
                 ) -> None:
        super().__init__("task_queue",
                         parent.profiler,
                         parent.timer)
        self.task_source = task_source
        self.queue: deque[Task] = deque()
        self.log.setLevel(logging.WARNING)

    def schedule_task(self, task: Task) -> None:  # type: ignore
        # Handle normal tasks
        self.dbg("Scheduling task %s", task)
        self.queue.appendleft(task)

    def get_next(self) -> Optional[Task]:
        """Take the next task off the queue
        """
        if self.is_empty():
            new_tasks = self.task_source()
            for t in new_tasks:
                self.schedule_task(t)
            else:
                return None
        next = self.queue.popleft()
        self.dbg("Next task: %s", next)
        self.dbg("%s tasks left in queue", len(self.queue))
        return next

    def get_new_tasks(self) -> SomeTasks:
        return self.task_source()

    def is_empty(self) -> bool:
        return len(self.queue) == 0
