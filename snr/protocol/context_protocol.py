import logging
from typing import Optional

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .component_protocol import ComponentProtocol
from .profiler_protocol import ProfilerProtocol


@runtime_checkable
class ContextProtocol(ComponentProtocol, Protocol):
    log: logging.Logger
    settings: Settings
    profiler: Optional[ProfilerProtocol]
