from typing import Any, Dict, List, Optional, Tuple, Union

from snr.config import Mode, Role
from snr.context import Context
from snr.dds.dds import DDS
from snr.dds.factory import DDSFactory
from snr.endpoint.endpoint import Endpoint
from snr.endpoint.factory import EndpointFactory
from snr.factory import Factory
from snr.root_context import RootContext
from snr.task import SomeTasks, Task, TaskHandler, TaskSource
from snr.task_queue import TaskQueue
from snr.utils.profiler import Profiler

SLEEP_TIME = 0.001
TASK_TYPE_TERMINATE = "terminate"


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
        dds_facs, endpoint_facs = self.seperate(factories)
        self.task_queue = TaskQueue(self, self.get_new_tasks)
        self.datastore = DDS(self,
                             dds_facs,
                             self.task_queue.schedule)
        (self.endpoints, self.task_producers) = self.get_all(endpoint_facs)
        self.task_handlers: Dict[str, TaskHandler] = {
            TASK_TYPE_TERMINATE: self.terminate_task_handler
        }
        self.terminate_flag: bool = False
        self.info("Initialized with {} endpoints",
                  [len(self.endpoints)])

    def loop(self):
        while not self.terminate_flag:
            if self.task_queue.is_empty():
                self.datastore.catch_up("idle_node_no_tasks")
            t: Optional[Task] = self.task_queue.get_next()
            if t:
                self.execute_task(t)
            else:
                self.sleep(SLEEP_TIME)

    def get_new_tasks(self):
        """Retrieve tasks from endpoints and queue them.
        """
        new_tasks: List[Task] = []
        for task_source in self.task_producers:
            t: SomeTasks = task_source()
            if t:
                if isinstance(t, Task):
                    new_tasks.append(t)
                else:
                    new_tasks.extend(t)
                self.dbg("Produced task: {} from {}",
                         [t, task_source])
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

        handler = self.task_handlers.get(t.task_type)
        if handler:
            result = self.time(t.task_type, handler, t)
            if result:
                if isinstance(result, Task):
                    new_tasks.append(result)
                else:
                    new_tasks.extend(result)
        # TODO: Store all task handlers in Node

        for e in self.endpoints:
            handler = e.task_handlers.get(t.task_type)
            if handler:
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
        self.dbg("Letting DDS catch up")
        self.datastore.catch_up("Scheduled tasks after execution")

    def terminate_task_handler(self, t: Task) -> SomeTasks:
        if ("all" in t.val_list
                or "node" in t.val_list):
            self.set_terminate_flag("terminate task")
        return None

    def set_terminate_flag(self, reason: str):
        self.info("Exit reason: {}", [reason])
        self.datastore.store("node_exit_reason", reason, False)
        self.terminate_flag = True
        for e in self.endpoints:
            e.set_terminate_flag(f"node: {reason}")

    def terminate(self):
        """Execute actions needed to deconstruct a Node.
        Terminate is executed the main thread or process of an object.
        Conversely, join may be called from an external context such as
        another thread or process.
        """

        for e in self.endpoints:
            e.join()

        self.info("Terminated all endpoints")

        self.datastore.dump_data()
        self.datastore.join()
        super().terminate()
        self.info("Node {} finished terminating", [self.role])

    def seperate(self,
                 factories: List[Factory]
                 ) -> Tuple[
            List[DDSFactory],
            List[EndpointFactory]]:
        dds_facs: List[DDSFactory] = []
        endpoint_facs: List[EndpointFactory] = []
        self.info("Seperating facs: {}", [factories])
        for f in factories:
            if isinstance(f, DDSFactory):
                dds_facs.append(f)
            elif isinstance(f, EndpointFactory):
                endpoint_facs.append(f)
        self.dbg("DDS facs: {}\n\t\t\tEndpoint facs: {}",
                 [dds_facs, endpoint_facs])
        return (dds_facs, endpoint_facs)

    def get_all(self,
                factories: List[EndpointFactory]
                ) -> Tuple[List[Endpoint], List[TaskSource]]:
        self.info("Adding components from {} factories", [len(factories)])
        endpoints = []
        task_producers = []
        for factory in factories:
            new_endpoints = factory.get(self)
            for endpoint in new_endpoints:
                endpoints.append(endpoint)
                task_producers.extend(endpoint.task_producers)
                self.info("{} added {}", [factory, endpoint])
        return endpoints, task_producers

    def store_data(self, key: str, data: Any, process: bool = True) -> None:
        self.datastore.store(key, data, process)

    def get_data(self, key: str) -> Union[Any, None]:
        return self.datastore.get(key)
