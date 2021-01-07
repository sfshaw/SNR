from threading import Event
from typing import Any, Dict, List, Optional, Union

from snr.config import Mode, Role
from snr.context.context import Context
from snr.context.root_context import RootContext
from snr.dds.dds import DDS
from snr.endpoint.endpoint import Endpoint
from snr.endpoint.node_core_endpoint import NodeCore
from snr.factory import Factory
from snr.task import SomeTasks, Task
from snr.task_queue import TaskQueue
from snr.utils.profiler import Profiler

SLEEP_TIME = 0.001


class Node(Context):
    def __init__(self,
                 parent: RootContext,
                 role: Role,
                 mode: Mode,
                 factories: List[Factory]
                 ) -> None:
        super().__init__(role + "_node",
                         parent,
                         Profiler(parent.debugger, parent.settings))
        self.role = role
        self.mode = mode

        self.task_queue = TaskQueue(self, self.get_new_tasks)
        self.datastore = DDS(self,
                             self.task_queue.schedule)
        self.endpoints = self.get_endpoints(factories)
        self.terminate_flag = Event()
        self.info("Initialized with {} endpoints",
                  [len(self.endpoints)])

    def loop(self):
        for endpoint in self.endpoints.values():
            endpoint.start()

        while not self.terminate_flag.is_set():
            if self.task_queue.is_empty():
                self.datastore.flush()
            t: Optional[Task] = self.task_queue.get_next()
            if t:
                self.execute_task(t)
            else:
                self.sleep(SLEEP_TIME)
        self.dbg("Node exiting main loop")
        self.__terminate()

    def get_new_tasks(self):
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

    def execute_task(self, t: Task):
        """Execute the given task

        Note that the task is passed in and can be provided on the fly rather
        than needing to be in the queue.
        """
        if not t:
            self.dbg("execute_task", "Tried to execute None")
            return

        new_tasks: List[Task] = []
        handlers = [e.task_handlers.get(t.task_type)
                    for e in self.endpoints.values()]
        handlers = [h for h in handlers if h]
        self.dbg("Got {} handlers for {} task: {}",
                 [len(handlers), t.task_type, handlers])
        new_tasks: List[Task] = []
        for handler in handlers:
            self.dbg("Executing {} task with {}", [t.task_type, handler])
            result = self.time(t.task_type, handler, t)
            if result:
                if isinstance(result, Task):
                    new_tasks.append(result)
                else:
                    new_tasks.extend(result)
        self.dbg("Task execution resulted in {} new tasks",
                 [len(new_tasks)])
        if new_tasks:
            self.task_queue.schedule(new_tasks)
        self.datastore.flush()

    def set_terminate_flag(self, reason: str):
        self.info("Exit reason: {}", [reason])
        self.datastore.store("node_exit_reason", reason, False)
        self.terminate_flag.set()
        for e in self.endpoints.values():
            e.set_terminate_flag(f"node: {reason}")

    def __terminate(self):
        """Execute actions needed to deconstruct a Node.
        Terminate is executed the main thread or process of an object.
        Conversely, join may be called from an external context such as
        another thread or process.
        """
        self.stdout.flush()
        for e in self.endpoints:
            e.join("node_terminate")

        self.info("Terminated all endpoints")

        self.datastore.join()
        self.datastore.dump_data()

        self.stdout.flush()
        super().terminate()
        self.info("Node {} finished terminating", [self.role])

    def get_endpoints(self,
                      factories: List[Factory]
                      ) -> Dict[str, Endpoint]:
        self.info("Adding components from {} factories", [len(factories)])
        endpoints: Dict[str, Endpoint] = {"node_core": NodeCore(None, self)}
        for factory in factories:
            new_endpoint = factory.get(self)
            endpoints[new_endpoint.name] = new_endpoint
            self.info("{} added {}", [factory, new_endpoint])
        return endpoints

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        self.datastore.store(key, data, process)

    def get_data(self, key: str) -> Union[Any, None]:
        return self.datastore.get_data(key)
