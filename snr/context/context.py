from snr.context.std_io import StdIo
import time
from typing import Any, Callable, List, Optional, Union

from snr.settings import Settings
from snr.utils.debug.channels import *
from snr.utils.debug.debugger import Debugger
from snr.utils.profiler import Profiler


class Context:

    def __init__(self,
                 name: str,
                 parent: Any,
                 profiler: Optional[Profiler] = None
                 ) -> None:
        self.name = name
        self.stdIo: StdIo = parent.stdIo
        self.debugger: Debugger = parent.debugger
        self.settings: Settings = parent.settings
        self.profiler: Optional[Profiler] = profiler

        if self.debugger and self.settings:
            pass
        else:
            raise Exception(f"FATAL: Incorrectly constructed context: {name}")

    def terminate(self):
        self.dbg("Terminating context {}", [self.name])
        self.terminate_profiler()
        print("Context terminated.")

    def terminate_profiler(self) -> None:
        if isinstance(self.profiler, Profiler):
            self.profiler.join()
            self.profiler.dump()

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
        self.debugger.debug_flush(self.name,
                                  INFO_CHANNEL,
                                  message,
                                  format_args)

    def dump(self,
             message: str,
             format_args: Union[List[Any], Any, None] = None):
        self.debugger.debug(self.name, DUMP_CHANNEL, message, format_args)

    def time(self,
             task_name: str,
             handler: Callable[[Any], Any],
             args: Any) -> Any:
        if self.profiler:
            return self.profiler.time(f"{task_name}:{self.name}",
                                      handler, args)
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

    # def debug_delay(self):
    #     self.sleep(self.settings.DEBUGGING_DELAY_S)
