import logging
from typing import Optional

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .profiler_protocol import ProfilerProtocol
from .timer_protocol import TimerProtocol


@runtime_checkable
class ContextProtocol(Protocol):
    name: ComponentName
    log: logging.Logger
    settings: Settings
    profiler: Optional[ProfilerProtocol]
    timer: TimerProtocol
