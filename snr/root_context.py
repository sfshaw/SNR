from snr.settings import Settings
from snr.utils.debug.channels import *
from snr.utils.debug.debugger import Debugger


class RootContext:
    def __init__(self, name: str) -> None:
        self.name = name
        self.settings = Settings()
        self.debugger: Debugger = Debugger(self.settings)

    def terminate(self):
        self.debugger.debug(self.name,
                            INFO_CHANNEL,
                            "Terminating root context {}",
                            [self.name])
        self.debugger.join()
        print("Context terminated.")
