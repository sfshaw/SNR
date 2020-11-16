from snr.context.std_io import StdIo
from snr.settings import Settings
from snr.utils.debug.channels import *
from snr.utils.debug.debugger import Debugger


class RootContext:
    def __init__(self, name: str) -> None:
        self.name = name
        self.settings = Settings()
        self.stdIo = StdIo(name)
        self.debugger: Debugger = Debugger(self.stdIo, self.settings)

    def __enter__(self):
        pass

    def __exit__(self):
        self.terminate()

    def terminate(self):
        self.debugger.debug(self.name,
                            INFO_CHANNEL,
                            "Terminating root context {}",
                            [self.name])
        # self.debugger.join()
        self.stdIo.join()
        print("Context terminated.")
