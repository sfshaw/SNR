import time
from typing import Any, Callable, List, Optional, Union

from snr.settings import Settings
from snr.utils.debug.channels import *
from snr.utils.debug.debugger import Debugger
from snr.utils.profiler import Profiler


class Context:

    def __init__(self,
                 name: str,
                 parent_context: Any,
                 debugger: Optional[Debugger] = None,
                 profiler: Optional[Profiler] = None,
                 settings: Settings = Settings()
                 ) -> None:
        self.name = name
        if not debugger:
            debugger = Debugger(settings)
        self.debugger = debugger
        self.profiler = profiler
        self.settings: Settings = settings
        if isinstance(parent_context, Context):
            self.parent_name = parent_context.name
            self.debugger = parent_context.debugger
            self.profiler = profiler
            self.settings = parent_context.settings
        elif (not self.debugger) or (not self.settings):
            print(f"FATAL: Incorrectly constructed context: {name}")

    def terminate(self):
        self.dbg("Terminating context {}", [self.name])
        if isinstance(self.profiler, Profiler):
            self.profiler.join()
            self.profiler.dump()
        self.debugger.join()
        print("Context terminated.")

    def fatal(self,
              message: str,
              format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, FATAL_CHANNEL, message, format_args)

    def err(self,
            message: str,
            format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, ERROR_CHANNEL, message, format_args)

    def warn(self,
             message: str,
             format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, WARNING_CHANNEL, message, format_args)

    def log(self,
            message: str,
            format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, LOG_CHANNEL, message, format_args)

    def dbg(self,
            message: str,
            format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, DEBUG_CHANNEL, message, format_args)

    def info(self,
             message: str,
             format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, INFO_CHANNEL, message, format_args)

    def dump(self,
             message: str,
             format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, DUMP_CHANNEL, message, format_args)

    def time(self,
             task_name: str,
             handler: Callable[[Any], Any],
             *args: Any) -> Any:
        if self.profiler:
            return self.profiler.time(f"{task_name}:{self.name}",
                                      lambda: handler(*args))
        else:
            return handler(*args)

    def sleep(self, time_s: float):
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

    def debug_delay(self):
        self.sleep(self.settings.DEBUGGING_DELAY_S)


def root_context(name: str) -> Context:
    settings = Settings()
    debugger = Debugger(settings)
    return Context(name=name,
                   parent_context=None,
                   debugger=debugger,
                   profiler=Profiler(debugger, settings),
                   settings=settings)
