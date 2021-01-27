from snr import *

CONSOLE_PORT: int = 54321
runner = SynchronusTestRunner(
    Config(Mode.TEST,
           {"test": [
               CommandReceiverFactory(CONSOLE_PORT),
               CommandProcessorFactory()
           ]}))
runner.run()
