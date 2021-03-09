import functools
import multiprocessing as mp
import operator
import time
from typing import Any, Dict, List, Optional, Tuple

from snr.protocol import *
from snr.type_defs import *

from .context import RootContext
from .endpoint import NodeCoreFactory
from .task_queue import TaskQueue
from .utils.timer import Timer

SLEEP_TIME_S = 0.000001


class Node(RootContext, NodeProtocol):
    def __init__(self,
                 role: Role,
                 config: ConfigProtocol,
                 ) -> None:
        super().__init__(role + "_node", config.mode)
        self.info("Initializing in mode %s", config.mode)
        self.role = role
        self.mode = config.mode
        self.profiler_getter: ProfilerGetter = config.get_profiler
        self.timer = Timer()
        self.__task_queue = TaskQueue(self, self.__get_new_tasks)
        self.__datastore: Dict[DataKey, Page] = {}
        self.endpoints: Dict[str, EndpointProtocol] = {}
        self.add_component(NodeCoreFactory())
        for factory in config.get(role):
            self.add_component(factory)
        self.__terminate_flag = mp.Event()
        self.__is_terminated = mp.Event()
        self.info("Initialized with %s endpoints",
                  len(self.endpoints))

    def loop(self) -> None:
        try:
            self.profiler = self.profiler_getter()
            for endpoint in self.endpoints.values():
                endpoint.start()

            while not self.__terminate_flag.is_set():
                t: Optional[Task] = self.__task_queue.get_next()
                if t:
                    self.__execute_task(t)
                else:
                    if SLEEP_TIME_S > 0:
                        time.sleep(SLEEP_TIME_S)
        finally:
            self.dbg("Node exiting main loop")
            self.terminate()

    def __get_new_tasks(self) -> SomeTasks:
        """Retrieve tasks from endpoints and queue them.
        """
        new_tasks: List[Task] = []
        for endpoint in self.endpoints.values():
            t: SomeTasks = endpoint.task_source()
            if t:
                if isinstance(t, Task):
                    new_tasks.append(t)
                else:
                    new_tasks.extend(t)
                self.dbg("Produced task: %s from %s",
                         t, endpoint)
        return new_tasks

    def __handle_task(self,
                      handler: TaskHandler,
                      t: Task,
                      k: TaskId
                      ) -> Optional[List[Task]]:
        self.dbg("Executing %s task with %s",
                 t.name, handler)
        result = self.profile(f"{t.type}({t.name})", handler, t, k)
        if isinstance(result, Task):
            return [result]
        else:
            return result

    def __execute_task(self, t: Task) -> None:
        handlers = self.get_task_handlers(t)
        self.dbg("Got %s handlers for %s task",
                 len(handlers), t.id())
        results: List[List[Task]] = list(filter(None,
                                                [self.__handle_task(h, t, k)
                                                 for (h, k) in handlers]))
        new_tasks: List[Task] = functools.reduce(operator.iconcat,
                                                 results,
                                                 [])
        self.dbg("Task execution resulted in %s new tasks",
                 len(new_tasks))
        if new_tasks:
            self.__task_queue.schedule(new_tasks)

    def get_task_handlers(self,
                          t: Task,
                          ) -> List[Tuple[TaskHandler, TaskId]]:
        return list(filter(None, map(lambda e: e.get_task_handler(t),
                                     self.endpoints.values())))

    def set_terminate_flag(self, reason: str) -> None:
        self.info("Setting terminate flag for: %s", reason)
        self.store_data("exit_reason", reason, False)
        self.__terminate_flag.set()
        for endpoint in self.endpoints.values():
            endpoint.set_terminate_flag()

    def terminate(self) -> None:
        """Execute actions needed to deconstruct a Node.
        Terminate is executed the main thread or process of an object.
        Conversely, join may be called from an external context such as
        another thread or process.
        """
        self.set_terminate_flag("terminate")
        if self.is_terminated():
            self.err("Already terminated")

        for e in self.endpoints.values():
            e.join()
            e.terminate()
        self.info("Terminated all %s endpoints",
                  len(self.endpoints))

        self.dbg(self.dump_data())

        self.terminate_context()

        self.__is_terminated.set()
        self.info("Node %s finished terminating", self.role)

    def is_terminated(self) -> bool:
        return self.__is_terminated.is_set()

    def add_component(self, factory: FactoryProtocol) -> Optional[str]:
        component = factory.get(self)
        if isinstance(component, EndpointProtocol):
            self.endpoints[component.name] = component
            self.info("%s added %s", factory, component)
            return component.name
        else:
            self.err("Unknown component type: %s", component)
            return None

    def schedule(self, t: SomeTasks) -> None:
        self.__task_queue.schedule(t)

    def synchronous_store(self, page: Page) -> None:
        self.check_main_thread(
            "Synchronous store called from outside main thread.")
        self.__datastore[page.key] = page
        self.dbg("Page stored: (%s)", page.key)

    def page(self, key: DataKey, data: Any, process: bool = True) -> Page:
        created_at = self.timer.current_s()
        return Page(key, data, self.name, created_at, process)

    def store_page(self, page: Page) -> None:
        self.schedule(task_store_page(page))

    def get_page(self, key: str) -> Optional[Page]:
        return self.__datastore.get(key)

    def get_time_s(self) -> float:
        return self.timer.current_s()

    def dump_data(self) -> str:
        lines = ["Datastore dump:"]
        for page in self.__datastore.values():
            lines.append(f"\t{page}")
        return "\n".join(lines)


__all__ = [
    "Node"
]
