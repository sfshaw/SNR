import logging
import threading
from abc import ABC
from typing import Any, Callable, Dict, Optional, TypeVar

from .abstract_profiler import AbstractProfiler
from .mode import Mode
from .names import str
from .timer_protocol import TimerProtocol

# Log Levels
LOG_LEVELS: Dict[Mode, int] = {
    Mode.TEST: logging.WARNING,
    Mode.DEBUG: logging.DEBUG,
    Mode.DEPLOYED: logging.INFO,
}


class AbstractContext(ABC):

    name: str
    log: logging.Logger
    profiler: Optional[AbstractProfiler]
    timer: TimerProtocol

    def fatal(self,
              message: str,
              *format_args: Any
              ) -> None:
        self.log.critical(message, *format_args, stack_info=True)

    def err(self,
            message: str,
            *format_args: Any
            ) -> None:
        self.log.error(message, *format_args, stack_info=True)

    def warn(self,
             message: str,
             *format_args: Any
             ) -> None:
        self.log.debug(message, *format_args)

    def dbg(self,
            message: str,
            *format_args: Any,
            ) -> None:
        self.log.debug(message, *format_args)

    def info(self,
             message: str,
             *format_args: Any,
             ) -> None:
        self.log.info(message, *format_args)

    T = TypeVar("T")

    def profile(self,
                task_name: str,
                handler: Callable[..., T],
                *args: Any) -> T:
        if self.profiler:
            return self.profiler.time(f"{task_name}:{handler.__module__}",
                                      handler, *args)
        else:
            return handler(*args)

    def check_main_thread(self, message: str) -> None:
        if threading.main_thread() != threading.current_thread():
            self.err(message)

    def __repr__(self) -> str:
        return self.name
