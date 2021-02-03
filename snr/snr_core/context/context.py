import logging

from snr.snr_protocol import *
from snr.snr_types import *


class Context(ContextProtocol):

    def __init__(self,
                 name: str,
                 parent: ContextProtocol,
                 profiler: Optional[ProfilerProtocol] = None
                 ) -> None:
        self.name = name

        self.log = logging.getLogger(self.name)

        self.settings = parent.settings
        self.profiler = profiler

    def terminate(self) -> None:
        self.dbg("Terminating context %s", self.name)
        if self.profiler:
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

    def profile(self,
                task_name: str,
                handler: Callable[..., T],
                *args: Any) -> T:
        if self.profiler:
            return self.profiler.time(f"{task_name}:{self.name}",
                                      handler, *args)
        else:
            return handler(*args)
