from typing import List, Optional

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

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
