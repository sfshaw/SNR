import functools
import logging
import multiprocessing as mp
import operator
from multiprocessing import synchronize
from typing import Any, Dict, List, Optional, Tuple

from snr.prelude import *

from . import tasks
from .contexts import RootContext
from .deque_task_queue import DequeTaskQueue as TaskQueImpl
from .node_core.node_core_factory import NodeCoreFactory
from .node_core.node_core_endpoint import NodeCoreEndpoint


class Node(RootContext, AbstractNode):

    role: Role
    config: AbstractConfig
    profiler: Optional[AbstractProfiler]
    components: Dict[str, AbstractComponent]
    __task_queue: AbstractTaskQueue
    __datastore: DataDict
    __terminate_flag: synchronize.Event
    __is_terminated: synchronize.Event

    def __init__(self,
                 role: Role,
                 config: AbstractConfig,
                 ) -> None:
        super().__init__(role + "_node", config.mode)
        self.log.setLevel(logging.WARNING)
        self.info("Initializing in mode %s", config.mode)
        self.role = role
        self.mode = config.mode
        self.config = config
        self.__task_queue = TaskQueImpl(self,
                                        self.get_new_tasks)
        self.__datastore = {}
        self.__terminate_flag = mp.Event()
        self.__is_terminated = mp.Event()
        core_endpoint: NodeCoreEndpoint = NodeCoreFactory().get(self)
        self.components = {
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
            self.profiler = self.config.get_profiler()
            for component in self.components.values():
                component.begin()

            while not self.__terminate_flag.is_set():
                t: Optional[Task] = self.__task_queue.get_next()
                if t:
                    self.execute_task(t)
        finally:
            self.dbg("Node exiting main loop")
            self.terminate()

    def get_new_tasks(self) -> List[Task]:
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
        empty_list: List[Task] = list()
        results = [self.handle_task(h, t, k)
                   for (h, k) in handlers]
        new_tasks: List[Task] = functools.reduce(
            operator.iconcat,
            [some_tasks
             for some_tasks in results
             if some_tasks],
            empty_list)
        self.dbg("Task execution resulted in %s new tasks",
                 len(new_tasks))
        if new_tasks:
            self.__task_queue.schedule(new_tasks)

    def get_task_handlers(self,
                          task: Task,
                          ) -> List[Tuple[TaskHandler, TaskId]]:
        maybe_handlers: List[Optional[Tuple[TaskHandler, TaskId]]] = \
            [components.get_task_handler(task)
             for components in self.components.values()]
        handlers: List[Tuple[TaskHandler, TaskId]] = \
            [handler_tuple
             for handler_tuple in maybe_handlers
             if handler_tuple]
        return handlers

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

    def get_page(self, key: DataKey) -> Optional[Page]:
        return self.__datastore.get(key)

    def get_time_s(self) -> float:
        return self.timer.current_s()

    def dump_data(self) -> str:
        lines = ["Datastore dump:"]
        for page in self.__datastore.values():
            lines.append(f"\t{page}")
        return "\n".join(lines)
