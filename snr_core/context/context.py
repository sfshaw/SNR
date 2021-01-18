from __future__ import annotations

import time
from typing import Any, Callable, List, Optional, TypeVar, Union

from snr_core.context.root_context import RootContext
from snr_core.context.stdout_consumer import StdOutConsumer
from snr_core.settings import Settings
from snr_core.utils.debug.channels import *
from snr_core.utils.debug.debugger import Debugger
from snr_core.utils.profiler import Profiler


class Context:

    def __init__(self,
                 name: str,
                 parent: Union[RootContext, Context],
                 profiler: Optional[Profiler] = None
                 ) -> None:
        self.name = name
        self.stdout: StdOutConsumer = parent.stdout
        self.debugger: Debugger = parent.debugger
        self.settings: Settings = parent.settings
        self.profiler: Optional[Profiler] = profiler

        if self.debugger and self.settings:
            pass
        else:
            raise Exception(f"FATAL: Incorrectly constructed context: {name}")

    def terminate(self) -> None:
        self.dbg("Terminating context {}", [self.name])
        if isinstance(self.profiler, Profiler):
            self.profiler.join_from("context temrinate")
            self.profiler.dump()
        self.info("Context {} terminated", [self.name])
        self.stdout.flush()

    def fatal(self,
              message: str,
              format_args: Union[List[Any], Any, None] = None
              ) -> None:
        self.debugger.debug(self.name, FATAL_CHANNEL, message, format_args)

    def err(self,
            message: str,
            format_args: Union[List[Any], Any, None] = None
            ) -> None:
        self.debugger.debug(self.name, ERROR_CHANNEL, message, format_args)

    def warn(self,
             message: str,
             format_args: Union[List[Any], Any, None] = None,
             flush: bool = False
             ) -> None:
        self.debugger.debug(self.name, WARNING_CHANNEL, message, format_args)
        if flush:
            self.flush()

    def log(self,
            message: str,
            format_args: Union[List[Any], Any, None] = None
            ) -> None:
        self.debugger.debug(self.name, LOG_CHANNEL, message, format_args)

    def dbg(self,
            message: str,
            format_args: Union[List[Any], Any, None] = None
            ) -> None:
        self.debugger.debug(self.name, DEBUG_CHANNEL, message, format_args)

    def info(self,
             message: str,
             format_args: Union[List[Any], Any, None] = None
             ) -> None:
        self.debugger.debug_flush(self.name,
                                  INFO_CHANNEL,
                                  message,
                                  format_args)

    def dump(self,
             message: str,
             format_args: Union[List[Any], Any, None] = None
             ) -> None:
        self.debugger.debug(self.name, DUMP_CHANNEL, message, format_args)

    def flush(self) -> None:
        self.debugger.flush()

    T = TypeVar("T")

    def time(self,
             task_name: str,
             handler: Callable[..., T],
             args: List[Any]) -> T:
        if self.profiler:
            return self.profiler.time(f"{task_name}:{self.name}",
                                      handler, args)
        else:
            return handler(*args)

    def sleep(self,
              time_s: float
              ) -> None:
        """Pauses the execution of the thread for time_s seconds
        """
        if self.settings.DISABLE_SLEEP:
            self.debugger.debug(f"{self.name}:sleep",
                                WARNING_CHANNEL,
                                "Sleep disabled, not sleeping")
            return
        if time_s == 0:
            return

        time.sleep(time_s)
