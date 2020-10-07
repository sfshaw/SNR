import time
from snr.utils.profiler import Profiler
from typing import Callable, Union

from snr.utils.debug.debugger import Debugger
from snr.utils.debug.debug import DEBUG_CHANNEL, DUMP_CHANNEL,  ERROR_CHANNEL, FATAL_CHANNEL, INFO_CHANNEL, LOG_CHANNEL, WARNING_CHANNEL
from snr.settings import Settings


class Context:

    def __init__(self,
                 name: str,
                 parent_context,
                 debugger: Debugger = None,
                 profiler: Profiler = None,
                 settings: Settings = Settings()):
        self.name = name
        if not debugger:
            debugger = Debugger(settings)
        self.debugger = debugger
        self.profiler = profiler
        self.settings: Settings = settings
        if parent_context:
            self.parent_name = parent_context.name
            self.debugger = parent_context.debugger
            self.profiler = profiler
            self.settings = parent_context.settings
        elif (not self.debugger) or (not self.settings):
            print(f"FATAL: Incorrectly constructed context: {name}")

    def terminate(self):
        self.dbg("Terminating context {}", [self.name])
        self.profiler.join()
        self.profiler.dump()
        self.debugger.join()
        print("Context terminated.")

    def fatal(self, *args: Union[list,  str]):
        self.debugger.debug(self.name, FATAL_CHANNEL, *args)

    def err(self, *args: Union[list,  str]):
        self.debugger.debug(self.name, ERROR_CHANNEL, *args)

    def warn(self, *args: Union[list,  str]):
        self.debugger.debug(self.name, WARNING_CHANNEL, *args)

    def log(self, *args: Union[list,  str]):
        self.debugger.debug(self.name, LOG_CHANNEL, *args)

    def dbg(self, *args: Union[list,  str]):
        self.debugger.debug(self.name, DEBUG_CHANNEL, *args)

    def info(self, *args: Union[list,  str]):
        self.debugger.debug(self.name, INFO_CHANNEL, *args)

    def dump(self, *args: Union[list,  str]):
        self.debugger.debug(self.name, DUMP_CHANNEL, *args)

    def time(self, task_name: str, handler: Callable, *args):
        if self.profiler:
            return self.profiler.time(f"{task_name}:{self.name}",
                                      lambda: handler(*args))
        else:
            return handler(*args)

    def sleep(self, time_s: float):
        """Pauses the execution of the thread for time_s seconds
        """
        if self.settings.DISABLE_SLEEP:
            # TODO: Elimanate debug dependancy from utils (will crash)
            self.debugger.debug(f"{self.name}:sleep",
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
