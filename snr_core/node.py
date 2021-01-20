from __future__ import annotations

from threading import Event
from typing import Any, Dict, List, Optional, Tuple, Union

from snr_core.config import Mode, Role
from snr_core.context.context import Context
from snr_core.context.root_context import RootContext
from snr_core.datastore.datastore import Datastore
from snr_core.endpoint.endpoint_base import EndpointBase
from snr_core.loop.loop_base import LoopBase
from snr_core.factory.factory_base import FactoryBase
from snr_core.endpoint.node_core_endpoint import NodeCore
from snr_core.task import SomeTasks, Task, TaskHandler, TaskId
from snr_core.task_queue import TaskQueue
from snr_core.utils.profiler import Profiler

SLEEP_TIME = 0.001


class Node(Context):
    def __init__(self,
                 parent: RootContext,
                 role: Role,
                 mode: Mode,
                 factories: List[FactoryBase]
                 ) -> None:
        super().__init__(role + "_node",
                         parent,
                         Profiler(parent.debugger, parent.settings))
        self.role = role
        self.mode = mode

        self.__task_queue = TaskQueue(self, self.__get_new_tasks)
        self.__datastore = Datastore(self, self.schedule)
        self.endpoints, self.loops = self.__get_components(factories)
        self.__terminate_flag = Event()
        self.is_terminated = Event()
        self.info("Initialized with {} endpoints",
                  [len(self.endpoints)])

    def loop(self):
        for endpoint in self.endpoints.values():
            endpoint.start()
        for loop in self.loops.values():
            loop.start()

        while not self.__terminate_flag.is_set():
            if self.__task_queue.is_empty():
                self.__datastore.flush()
            t: Optional[Task] = self.__task_queue.get_next()
            if t:
                self.__execute_task(t)
            else:
                self.sleep(SLEEP_TIME)
        self.dbg("Node exiting main loop")
        self.terminate()

    def __get_new_tasks(self):
        """Retrieve tasks from endpoints and queue them.
        """
        new_tasks: List[Task] = []
        for endpoint in self.endpoints.values():
            for task_producer in endpoint.task_producers:
                t: SomeTasks = task_producer()
                if t:
                    if isinstance(t, Task):
                        new_tasks.append(t)
                    else:
                        new_tasks.extend(t)
                    self.dbg("Produced task: {} from {}",
                             [t, endpoint])
        return new_tasks

    def __execute_task(self, t: Task):
        if not t:
            self.dbg("execute_task", "Tried to execute None")
            return

        new_tasks: List[Task] = []
        handlers = self.get_task_handlers(t)

        self.dbg("Got {} handlers for {} task: {}",
                 [len(handlers), t.name, handlers])
        new_tasks: List[Task] = []
        for (handler, key) in handlers:
            self.dbg("Executing {} task with {}", [t.name, handler])
            result = self.time(t.name, handler, [t, key])
            if result:
                if isinstance(result, Task):
                    new_tasks.append(result)
                else:
                    new_tasks.extend(result)
        self.dbg("Task execution resulted in {} new tasks",
                 [len(new_tasks)])
        if new_tasks:
            self.__task_queue.schedule(new_tasks)
        self.__datastore.flush()

    def get_task_handlers(self, t: Task) -> List[Tuple[TaskHandler, TaskId]]:
        maybe_handlers_and_keys = [e.get_task_handler(t)
                                   for e in self.endpoints.values()]
        return [(handler, key)
                for (handler, key) in maybe_handlers_and_keys
                if handler]

    def set_terminate_flag(self, reason: str):
        self.info("Setting terminate flag for: {}", [reason])
        self.__datastore.store("node_exit_reason", reason, False)
        self.__datastore.flush()
        self.__terminate_flag.set()
        # for e in self.endpoints.values():
        #     e.set_terminate_flag()
        for l in self.loops.values():
            l.set_terminate_flag()

    def terminate(self):
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
        self.stdout.flush()

        for e in self.endpoints.values():
            e.terminate()
        for l in self.loops.values():
            l.join()

        self.info("Terminated all endpoints")

        self.__datastore.join()
        self.__datastore.dump_data()

        self.stdout.flush()
        super().terminate()
        self.is_terminated.set()
        self.info("Node {} finished terminating", [self.role])

    def __get_components(self,
                         factories: List[FactoryBase]
                         ) -> Tuple[Dict[str, EndpointBase],
                                    Dict[str, LoopBase]]:
        self.info("Adding components from {} factories", [len(factories)])
        endpoints: Dict[str, EndpointBase] = {
            "node_core": NodeCore(None, self)}
        loops: Dict[str, LoopBase] = {}
        for factory in factories:
            component = factory.get(self)
            if isinstance(component, EndpointBase):
                endpoints[component.name] = component
            else:
                loops[component.name] = component
            self.info("{} added {}", [factory, component])
        return endpoints, loops

    def schedule(self, t: Task) -> None:
        self.__task_queue.schedule(t)

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        self.__datastore.store(key, data, process)

    def get_data(self, key: str) -> Union[Any, None]:
        return self.__datastore.get_data(key)
