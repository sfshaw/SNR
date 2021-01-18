from __future__ import annotations

from typing import Any, Optional

from snr_core.context.stdout import StdOut
from snr_core.context.stdout_consumer import StdOutConsumer
from snr_core.settings import Settings
from snr_core.utils.debug.channels import *
from snr_core.utils.debug.debugger import Debugger


class RootContext:
    def __init__(self,
                 name: str,
                 stdout: Optional[StdOutConsumer] = None
                 ) -> None:
        self.name = name
        self.settings = Settings()
        self.owned_stdio: bool = False
        if not stdout:
            self.owned_stdio = True
            stdout = StdOut(name)
        self.stdout: StdOutConsumer = stdout
        self.debugger: Debugger = Debugger(self.stdout, self.settings)

    def __enter__(self) -> RootContext:
        return self

    def __exit__(self,
                 exc_type: Any,
                 exc_value: Any,
                 traceback: Any
                 ):
        if exc_type or exc_value or traceback:
            self.debugger.debug(
                self.name,
                WARNING_CHANNEL,
                "Exiting context (exc_type: {},\texec_val: {}\ttraceback: {})",
                [exc_type, exc_value, traceback])
        self.terminate()

    def terminate(self):
        self.debugger.debug(self.name,
                            INFO_CHANNEL,
                            "Terminating root context")
        if self.owned_stdio:
            self.stdout.join_from(self.name)
            print("Context terminated.")
        else:
            self.stdout.flush()
            self.debugger.debug(self.name,
                                INFO_CHANNEL,
                                "Unowned StdIO not joined/terminated")
