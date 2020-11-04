from queue import Queue
from typing import List, Union

from snr.context import Context
from snr.task import SomeTasks, Task, TaskSource


class TaskQueue(Context):
    def __init__(self,
                 parent_context: Context,
                 task_source: TaskSource):
        super().__init__("task_queue", parent_context)
        self.get_new_tasks = task_source
        self.queue: "Queue[Task]" = Queue()

    def schedule(self, t: SomeTasks) -> None:
        """ Adds a Task or a list of Tasks to the node's queue
        """
        if isinstance(t, Task):
            self.__schedule_task(t)
            return
        if isinstance(t, List):
            # Recursively handle lists
            self.dbg("Recursively scheduling list of {} tasks",
                     [len(t)])
            for item in t:
                self.schedule(item)
            return
        if not t:
            if t is None:
                self.warn("Cannot schedule None or empty list")
                return
        self.err("Cannot schedule {} object {}", [type(t), t])

    def __schedule_task(self, t: Task) -> None:
        # Handle normal tasks
        self.dbg("Scheduling task {}", [t])
        # Ignore Priority
        self.queue.put(t)
        # TODO: Use priority with multiprocessing queue
        # if t.priority == TaskPriority.high:
        #     self.queue.put(t)  # High priotity at front (right)
        # elif t.priority == TaskPriority.normal:
        #     self.queue.put(t)  # Normal priotity at end (left)
        #     # TODO:  insert normal priority in between high and low
        # elif t.priority == TaskPriority.low:
        #     self.queue.put(t)  # Normal priotity at end (left)
        # else:
        #     self.err( "Cannot schedule task with priority: {}",
        #              [t.priority])

    def get_next(self) -> Union[Task, None]:
        """Take the next task off the queue
        """
        if self.queue.empty():
            self.info("Ran out of tasks, getting more")
            new_tasks = self.get_new_tasks()
            if new_tasks:
                self.schedule(new_tasks)
            else:
                return None
        return self.queue.get()
