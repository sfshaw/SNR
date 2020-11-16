from snr.config import Config
from snr.io.console.factory import ConsoleFactory
from snr.runner.test_runner import SynchronusTestRunner

runner = SynchronusTestRunner(Config({
    "test": [ConsoleFactory()]}))
runner.run()
