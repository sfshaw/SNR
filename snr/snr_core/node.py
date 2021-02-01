import functools
import logging
import operator
import time
from threading import Event

from snr.snr_protocol import *

from .context.context import Context
from .context.root_context import RootContext
from .datastore import Datastore
from .endpoint.node_core_factory import NodeCoreFactory
from .task_queue import TaskQueue
from .utils.profiler import Profiler

SLEEP_TIME = 0.00005


class Node(Context, NodeProtocol):
    def __init__(self,
                 parent: RootContext,
                 role: Role,
                 mode: Mode,
                 factories: List[FactoryProtocol],
                 ) -> None:
        super().__init__(role + "_node",
                         parent,
                         Profiler(parent.settings))
        self.log.setLevel(logging.WARN)
        self.role = role
        self.mode = mode
        self.context = self
        self.__task_queue = TaskQueue(self, self.__get_new_tasks)
        self.__datastore = Datastore(self, self.schedule)
        self.endpoints: Dict[str, EndpointProtocol] = {}
        self.add_component(NodeCoreFactory())
        for factory in factories:
            self.add_component(factory)
        self.__terminate_flag = Event()
        self.is_terminated = Event()
        self.info("Initialized with %s endpoints",
                  len(self.endpoints))

    def loop(self) -> None:
        for endpoint in self.endpoints.values():
            endpoint.start()

        while not self.__terminate_flag.is_set():
            # if self.__task_queue.is_empty():
            #     self.__datastore.flush()
            t: Optional[Task] = self.__task_queue.get_next()
            if t:
                self.__execute_task(t)
            else:
                if SLEEP_TIME > 0:
                    time.sleep(SLEEP_TIME)

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
        result = self.profile(t.name, handler, [t, k])
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

    def get_task_handlers(self, t: Task) -> List[Tuple[TaskHandler, TaskId]]:
        return list(filter(None, map(lambda e: e.get_task_handler(t),
                                     self.endpoints.values())))

    def set_terminate_flag(self, reason: str) -> None:
        self.info("Setting terminate flag for: %s", reason)
        self.__datastore.synchronous_store(self.__datastore.page("exit_reason",
                                                                 reason,
                                                                 False))
        self.__terminate_flag.set()
        for endpoint in self.endpoints.values():
            endpoint.set_terminate_flag()

    def terminate(self) -> None:
        """Execute actions needed to deconstruct a Node.
        Terminate is executed the main thread or process of an object.
        Conversely, join may be called from an external context such as
        another thread or process.
        """
        if not self.__terminate_flag.is_set():
            self.warn("Temrinated prior to setting of terminate flag")
            self.set_terminate_flag("terminate")
        if self.is_terminated.is_set():
            self.err("Already terminated")

        for e in self.endpoints.values():
            e.join()
        self.info("Terminated all %s endpoints",
                  len(self.endpoints))

        self.__datastore.dump_data()

        super().terminate()
        self.is_terminated.set()
        self.info("Node %s finished terminating", self.role)

    def add_component(self, factory: FactoryProtocol) -> Optional[str]:
        component = factory.get(self)
        if isinstance(component, EndpointProtocol):
            self.endpoints[component.name] = component
            return component.name
        else:
            self.err("Unknown component type: %s", component)
        self.info("%s added %s", factory, component)
        return None

    def schedule(self, t: SomeTasks) -> None:
        self.__task_queue.schedule(t)

    def synchronous_store(self, page: Page) -> None:
        self.__datastore.synchronous_store(page)

    def store_page(self, page: Page) -> None:
        self.schedule(task.store_page(page))

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        self.store_page(self.__datastore.page(key, data, process))

    def get_data(self, key: str) -> Optional[Any]:
        return self.__datastore.get_data(key)

    def get_page(self, key: str) -> Optional[Page]:
        return self.__datastore.get_page(key)
