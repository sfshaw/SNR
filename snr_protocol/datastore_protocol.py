from typing import Any, Optional, Protocol

from snr_types import *


class DatastoreProtocol(Protocol):

    def store(self, key: str, value: Any, process: bool = True) -> None:
        ...

    def get_data(self, key: str) -> Optional[Any]:
        ...

    def get_page(self, key: str) -> Optional[Page]:
        ...

    def inbound_store(self, page: Page) -> None:
        ...

    def flush(self) -> None:
        ...

    def dump_data(self) -> None:
        ...

    def set_terminate_flag(self, reason: str) -> None:
        ...

    def join(self) -> None:
        ...