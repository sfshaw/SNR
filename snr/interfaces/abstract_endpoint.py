from abc import ABC, abstractmethod
from typing import Any, Optional

from snr.type_defs import *

from .abstract_component import AbstractComponent
from .abstract_factory import AbstractFactory
from .abstract_node import AbstractNode


class AbstractEndpoint(AbstractComponent, ABC):

    factory: AbstractFactory
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

    def store_page(self, page: Page) -> None:
        self.parent.store_page(page)

    def page(self,
             key: DataKey,
             data: Any,
             process: bool = True,
             ) -> Page:
        '''Page constructor
        '''
        return self.parent.page(key, data, process)

    def task_store_data(self,
                        key: DataKey,
                        data: Any,
                        process: bool = True,
                        ) -> Task:
        return self.parent.task_store_data(key, data, process)

    def task_store_page(self, page: Page) -> None:
        self.parent.task_store_page(page)

    def store_data(self,
                   key: DataKey,
                   data: Any,
                   process: bool = True,
                   ) -> None:
        return self.store_page(self.parent.page(key, data, process))

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
