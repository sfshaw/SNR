import logging

from snr.types import *

from .component_protocol import ComponentProtocol
from .profiler_protocol import ProfilerProtocol


@runtime_checkable
class ContextProtocol(ComponentProtocol, Protocol):
    log: logging.Logger
    settings: Settings
    profiler: Optional[ProfilerProtocol]

    def __enter__(self) -> "ContextProtocol":
        ...

    def __exit__(self, *args: Any) -> None:
        ...
