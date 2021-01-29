from snr.snr_core.config import Config
from snr.snr_core.runner.synchronus_runner import SynchronousRunner


class SynchronusTestRunner(SynchronousRunner):

    def __init__(self,
                 config: Config
                 ) -> None:
        super().__init__("test", config)
