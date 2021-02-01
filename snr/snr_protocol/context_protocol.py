from snr.snr_types import *

from .component_protocol import ComponentProtocol
from .profiler_protocol import ProfilerProtocol


@runtime_checkable
class ContextProtocol(ComponentProtocol, Protocol):
    settings: Settings
    profiler: Optional[ProfilerProtocol]
