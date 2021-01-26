from __future__ import annotations

import logging
import time
from typing import Any, Callable, List, Optional, TypeVar, Union

from snr_core.context.root_context import RootContext
from snr_core.settings import Settings
from snr_core.utils.profiler import Profiler


class Context:

    def __init__(self,
                 name: str,
                 parent: Union[RootContext, Context],
                 profiler: Optional[Profiler] = None
                 ) -> None:
        self.name = name

        self.log = logging.getLogger(self.name)

        self.settings: Settings = parent.settings
        self.profiler: Optional[Profiler] = profiler

        if not self.settings:
            raise Exception(f"FATAL: Incorrectly constructed context: {name}")

    def terminate(self) -> None:
        self.dbg("Terminating context %s", self.name)
        if isinstance(self.profiler, Profiler):
            self.profiler.join_from("context temrinate")
            self.profiler.dump()
        self.info("Context %s terminated", self.name)

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

    def dump(self,
             message: str,
             *format_args: Any
             ) -> None:
        self.log.info(message, *format_args)

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
        if time_s == 0:
            return

        time.sleep(time_s)
