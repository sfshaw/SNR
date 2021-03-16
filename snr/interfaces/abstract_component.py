from abc import ABC, abstractmethod

from snr.type_defs import *

from .abstract_factory import AbstractFactory
from .abstract_context import AbstractContext
from .task_interfaces import (ProvidesTaskHandlers, ProvidesTasks,
                              SchedulesTasks)


# @runtime_checkable
class AbstractComponent(AbstractContext,
                        ProvidesTaskHandlers,
                        ProvidesTasks,
                        SchedulesTasks,
                        ABC):
    factory: AbstractFactory

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
    def store_page(self, page: Page) -> None:
        ...
