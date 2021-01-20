from snr_core.config import Config, Mode
from snr.io.console.factory import (CommandProcessorFactory,
                                    CommandReceiverFactory)
from snr_core.runner.test_runner import SynchronusTestRunner

CONSOLE_PORT: int = 54321
runner = SynchronusTestRunner(
    Config(Mode.TEST,
           {"test": [
               CommandReceiverFactory(CONSOLE_PORT),
               CommandProcessorFactory()
           ]}))
runner.run()
