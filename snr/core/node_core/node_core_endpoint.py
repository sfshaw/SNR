
import logging
from typing import Any, List

from snr.prelude import *

from .. import tasks
from ..endpoints import Endpoint, EndpointFactory


class NodeCoreEndpoint(Endpoint):
    '''The `NodeCoreEndpoint` is a concrete `Endpoint` implementation used to
     provide task handling capabilities to the `Node`.

    All `Node`s construct their own `NodeCoreEndpoint`. Moving this
    capability to a separate class keeps the implementation of `Node` simpler
    and cleaner. As an `Enpoint` with a `Factory`, a `Node`'s `NodeCoreEndoint`
    can be reloaded during development.
    '''

    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "node_core")
        self.log.setLevel(logging.WARNING)
        self.task_handlers = {
            TaskType.terminate: self.task_handler_terminate,
            TaskType.store_page: self.task_handler_store_page,
            TaskType.reload: self.task_handler_reload,
            (TaskType.event, tasks.ADD_COMPONENT_TASK_NAME):
            self.task_handler_add_component,
            (TaskType.event, tasks.REMOVE_ENDPOINT_TASK_NAME):
                self.task_handler_remove_endpoint,
        }

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def task_source(self) -> List[Task]:
        return []

    def task_handler_store_page(self, t: Task, _key: TaskId) -> SomeTasks:
        assert isinstance(t.val_list[0], Page)
        page: Page = t.val_list[0]
        self.parent.synchronous_store(page)
        if page.process:
            return Task(TaskType.process_data, page.key)
        return None

    def task_handler_terminate(self, t: Task, key: TaskId) -> SomeTasks:
        # if ("all" in t.val_list
        #         or self.parent_node.name in t.val_list
        #         or "node" in t.val_list):
        self.parent.set_terminate_flag(f"terminate_task:{t.name}")
        return None

    def task_handler_reload(self, task: Task, key: TaskId) -> SomeTasks:
        target_name = task.name
        if target_name in self.parent.components.keys():
            self.info("Reloading component: %s", target_name)
            target = self.parent.components.pop(target_name)
            target.join()
            target.factory.reload()
            return tasks.add_component(target.factory)
        else:
            self.warn("Components %s not found", target_name)

        return None

    def task_handler_add_component(self, task: Task, key: TaskId) -> SomeTasks:
        assert (isinstance(task.val_list[0], AbstractFactory) and
                isinstance(task.val_list[1], bool))
        factory: AbstractFactory[Any] = task.val_list[0]
        start_component: bool = task.val_list[1]
        new_component = factory.get(self.parent)
        if new_component:
            self.parent.components[new_component.name] = new_component
            if start_component:
                new_component.begin()
            self.info("Added component %s", new_component.name)
        else:
            self.warn("Failed to get component from %s", factory)
        return None

    def task_handler_remove_endpoint(self,
                                     task: Task,
                                     key: TaskId,
                                     ) -> SomeTasks:
        target_name = task.val_list[0]
        self.info("Removing component %s", target_name)
        target = self.parent.components.pop(target_name)
        target.join()
        target.terminate()
        return None
