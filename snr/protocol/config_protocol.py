from snr.types import *

from .factory_protocol import FactoryProtocol
from .profiler_protocol import ProfilerProtocol


@runtime_checkable
class ConfigProtocol(Protocol):
    mode: Mode
    settings: Settings

    def get(self, role: str) -> List[FactoryProtocol]:
        ...

    def get_profiler(self) -> Optional[ProfilerProtocol]:
        ...
