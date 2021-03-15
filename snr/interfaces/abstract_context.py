import logging
from abc import ABC
from typing import Optional

from snr.type_defs import *

from .abstract_profiler import AbstractProfiler
from .timer_protocol import TimerProtocol


class AbstractContext(ABC):
    name: ComponentName
    log: logging.Logger
    settings: Settings
    profiler: Optional[AbstractProfiler]
    timer: TimerProtocol
