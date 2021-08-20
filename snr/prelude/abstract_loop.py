from abc import ABC, abstractmethod
from typing import Any

from .abstract_component import AbstractComponent
from .abstract_factory import AbstractFactory
from .abstract_node import AbstractNode
from .page import DataKey
from .task import SomeTasks, TaskHandlerMap


class AbstractLoop(AbstractComponent, ABC):
    """A Node component that runs outside the main thread event loop.

    Base loop implementation may use any concurrency style, ThreadLoop is
    provided. User implemented loops will inherit from base loops such as
    ThreadLoop.

    The loop lifecycle:
    Main thread                             Loop context
    1. Loop() - Constructed
    2. begin() - Started by Node
                                            3. setup() - Runs user setup
                                            4. loop_handler() - Runs its loop
    4. join() - Called from outside the
                loop to end it
    5. set_terminate_flag() - Signals loop
                              to end
                                            5. halt() - Cleans up after the
                                                        running loop, should
                                                        be reloadable now
    6. terminate() - Called by the Node to
                     clean the entire
                     module up

    The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """
    factory: AbstractFactory['AbstractLoop']
    parent: AbstractNode
    task_handlers: TaskHandlerMap
    delay_s: float

    @abstractmethod
    def setup(self) -> None:
        '''User implemented method run at the beginning of the Loop's loop
        '''
        ...

    @abstractmethod
    def loop(self) -> None:
        '''User implemented method run per loop iteration
        '''
        ...

    @abstractmethod
    def set_terminate_flag(self) -> None:
        '''Base loop function to signal termination, used by join()
        '''
        ...

    @abstractmethod
    def is_terminated(self) -> bool:
        '''Base loop function to indicate whether loop execution has finished
        '''
        ...

    def schedule(self, t: SomeTasks) -> None:
        self.parent.schedule(t)

    def store_data(self,
                   key: DataKey,
                   data: Any,
                   process: bool = True,
                   ) -> None:
        self.parent.store_data(key, data, process)
