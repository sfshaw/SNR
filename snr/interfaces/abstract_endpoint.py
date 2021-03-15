from abc import ABC, abstractmethod
from typing import Any, Optional

from snr.type_defs import *

from .abstract_component import AbstractComponent
from .abstract_node import AbstractNode


# @runtime_checkable
class AbstractEndpoint(AbstractComponent, ABC):
    parent: AbstractNode

    @abstractmethod
    def task_source(self) -> SomeTasks:
        ...

    def join(self) -> None:
        self.halt()

    @abstractmethod
    def halt(self) -> None:
        '''Non-destructive clean up method
        '''
        ...

    @abstractmethod
    def terminate(self) -> None:
        '''Desctructive clean up method
        '''
        ...

    def schedule(self, t: SomeTasks) -> None:
        self.parent.schedule(t)

    def page(self,
             key: DataKey,
             data: Any,
             process: bool = True,
             ) -> Page:
        '''Page constructor
        '''
        return Page(key, data,
                    self.name,
                    self.timer.current_s(),
                    process)

    # @abstractmethod
    # def task_store_data(self,
    #                     key: DataKey,
    #                     data: Any,
    #                     process: bool = True,
    #                     ) -> Task:
    #     ...

    # @abstractmethod
    # def task_store_page(self, page: Page) -> None:
    #     ...

    def get_page(self, key: DataKey) -> Optional[Page]:
        '''Thread-safe accesor for pages.
        '''
        return self.parent.get_page(key)

    def get_data(self, key: DataKey) -> Optional[Any]:
        '''Thread-safe accessor for plain data, wraps `get_page()`
        '''
        page = self.get_page(key)
        if page:
            return page.data
        return None
