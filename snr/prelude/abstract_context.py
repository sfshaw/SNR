import logging
from abc import ABC
from typing import Dict, Optional

from .names import ComponentName
from .mode import Mode

from .abstract_profiler import AbstractProfiler
from .timer_protocol import TimerProtocol

# Log Levels
LOG_LEVELS: Dict[Mode, int] = {
    Mode.TEST: logging.WARNING,
    Mode.DEBUG: logging.DEBUG,
    Mode.DEPLOYED: logging.INFO,
}


class AbstractContext(ABC):

    name: ComponentName
    log: logging.Logger
    profiler: Optional[AbstractProfiler]
    timer: TimerProtocol
