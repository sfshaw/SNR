from abc import ABC, abstractmethod
from typing import Any

from .abstract_context import AbstractContext
from .abstract_factory import AbstractFactory
from .page import DataKey
# from .task_interfaces import (ProvidesTaskHandlers, ProvidesTasks,
#                               SchedulesTasks)
from .task import TaskSource


class AbstractComponent(AbstractContext,
                        # ProvidesTaskHandlers,
                        # ProvidesTasks,
                        # SchedulesTasks,
                        ABC):

    factory: AbstractFactory[Any]
    task_source: TaskSource

    @abstractmethod
    def begin(self) -> None:
        ...

    @abstractmethod
    def join(self) -> None:
        ...

    @abstractmethod
    def halt(self) -> None:
        ...

    @abstractmethod
    def terminate(self) -> None:
        ...

    @abstractmethod
    def store_data(self,
                   key: DataKey,
                   data: Any,
                   process: bool = True,
                   ) -> None:
        ...
