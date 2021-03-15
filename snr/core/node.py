import functools
import logging
import multiprocessing as mp
import operator
import time
from typing import Any, Dict, List, Optional, Tuple

from snr.interfaces import *
from snr.type_defs import *

from . import tasks
from .contexts import RootContext
from .node_core.node_core_factory import NodeCoreFactory
from .task_queue import TaskQueue

# SLEEP_TIME_S: float = 0.000001
SLEEP_TIME_S: float = 0


class Node(RootContext, AbstractNode):
    def __init__(self,
                 role: Role,
                 config: AbstractConfig,
                 ) -> None:
        super().__init__(role + "_node", config.mode)
        self.log.setLevel(logging.WARNING)
        self.info("Initializing in mode %s", config.mode)
        self.role = role
        self.mode = config.mode
        self.profiler_getter: ProfilerGetter = config.get_profiler
        self.__task_queue = TaskQueue(self, self.get_new_tasks)
        self.__datastore: Dict[DataKey, Page] = {}
        core_endpoint = NodeCoreFactory().get(self)
        self.components: Dict[ComponentName, AbstractComponent] = {
            core_endpoint.name: core_endpoint,
        }
        for factory in config.get(role):
            core_endpoint.task_handler_add_component(
                tasks.add_component(factory, start_component=False),
                (TaskType.event, tasks.ADD_COMPONENT_TASK_NAME))
        self.__terminate_flag = mp.Event()
        self.__is_terminated = mp.Event()
        self.info("Initialized with %s endpoints",
                  len(self.components))

    def loop(self) -> None:
        try:
            self.profiler = self.profiler_getter()
            for endpoint in self.components.values():
                endpoint.begin()

            while not self.__terminate_flag.is_set():
                t: Optional[Task] = self.__task_queue.get_next()
                if t:
                    self.execute_task(t)
                else:
                    if SLEEP_TIME_S > 0:
                        time.sleep(SLEEP_TIME_S)
        finally:
            self.dbg("Node exiting main loop")
            self.terminate()

    def get_new_tasks(self) -> SomeTasks:
        new_tasks: List[Task] = []
        for component in self.components.values():
            t: SomeTasks = component.task_source()
            if t:
                if isinstance(t, Task):
                    new_tasks.append(t)
                else:
                    new_tasks.extend(t)
                self.dbg("Produced task: %s from %s",
                         t, component)
        return new_tasks

    def handle_task(self,
                    handler: TaskHandler,
                    task: Task,
                    key: TaskId,
                    ) -> Optional[List[Task]]:
        self.dbg("Executing %s task with %s",
                 task.name, handler)
        result = self.profile(f"{task.type}({task.name})", handler, task, key)
        if isinstance(result, Task):
            return [result]
        else:
            return result

    def execute_task(self, t: Task) -> None:
        handlers = self.get_task_handlers(t)
        self.dbg("Got %s handlers for %s task",
                 len(handlers), t.id())
        new_tasks: List[Task] = functools.reduce(
            operator.iconcat,
            filter(None,
                   [self.handle_task(h, t, k)
                    for (h, k) in handlers]),
            list())
        self.dbg("Task execution resulted in %s new tasks",
                 len(new_tasks))
        if new_tasks:
            self.__task_queue.schedule(new_tasks)

    def get_task_handlers(self,
                          task: Task,
                          ) -> List[Tuple[TaskHandler, TaskId]]:
        return list(filter(None, map(lambda e: e.get_task_handler(task),
                                     self.components.values())))

    def set_terminate_flag(self, reason: str) -> None:
        self.info("Setting terminate flag for: %s", reason)
        self.store_data("exit_reason", reason, False)
        self.__terminate_flag.set()
        # for endpoint in self.components.values():
        #     endpoint.set_terminate_flag()

    def terminate(self) -> None:
        """Execute actions needed to deconstruct a Node.
        Terminate is executed the main thread or process of an object.
        Conversely, join may be called from an external context such as
        another thread or process.
        """
        self.set_terminate_flag("terminate")
        if self.is_terminated():
            self.err("Already terminated")

        for component in self.components.values():
            component.join()
            component.terminate()
        self.info("Terminated all %s endpoints",
                  len(self.components))

        self.dbg(self.dump_data())

        self.terminate_context()

        self.__is_terminated.set()
        self.info("Node %s finished terminating", self.role)

    def is_terminated(self) -> bool:
        return self.__is_terminated.is_set()

    def schedule(self, t: SomeTasks) -> None:
        self.__task_queue.schedule(t)

    def page(self,
             key: DataKey,
             data: Any,
             process: bool = True,
             ) -> Page:
        created_at = self.timer.current_s()
        return Page(key, data, self.name, created_at, process)

    def synchronous_store(self, page: Page) -> None:
        self.check_main_thread(
            "Synchronous store called from outside main thread.")
        self.__datastore[page.key] = page
        self.dbg("Page stored: (%s)", page.key)

    def store_page(self, page: Page) -> None:
        self.schedule(tasks.store_page(page))

    def get_page(self, key: DataKey) -> Optional[Page]:
        return self.__datastore.get(key)

    def get_time_s(self) -> float:
        return self.timer.current_s()

    def dump_data(self) -> str:
        lines = ["Datastore dump:"]
        for page in self.__datastore.values():
            lines.append(f"\t{page}")
        return "\n".join(lines)
