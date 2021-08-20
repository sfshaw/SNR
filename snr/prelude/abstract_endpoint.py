from abc import ABC, abstractmethod
from typing import Any, Optional

from .abstract_component import AbstractComponent
from .abstract_factory import AbstractFactory
from .abstract_node import AbstractNode
from .page import DataKey, Page
from .task import SomeTasks


class AbstractEndpoint(AbstractComponent, ABC):

    factory: AbstractFactory['AbstractEndpoint']
    parent: AbstractNode

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
        return self.parent.page(key, data, process)

    def store_data(self,
                   key: DataKey,
                   data: Any,
                   process: bool = True,
                   ) -> None:
        return self.parent.store_data(key, data, process)

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
