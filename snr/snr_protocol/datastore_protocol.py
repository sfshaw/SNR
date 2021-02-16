from snr.snr_types import *


@runtime_checkable
class DatastoreProtocol(Protocol):

    def page(self, key: str, value: Any, process: bool = True) -> Page:
        ...

    def get_data(self, key: str) -> Optional[Any]:
        ...

    def get_page(self, key: str) -> Optional[Page]:
        ...

    def synchronous_store(self, page: Page) -> None:
        ...

    def dump_data(self) -> None:
        ...
