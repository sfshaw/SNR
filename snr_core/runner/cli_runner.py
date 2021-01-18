import sys

from snr_core.config import Config, Mode
from snr_core.runner.synchronus_runner import SynchronousRunner
from snr_core.utils.utils import print_usage


class CLIRunner(SynchronousRunner):

    def __init__(self, config: Config):
        argc = len(sys.argv)
        if argc < 2:
            print_usage()
            sys.exit(1)
        role = sys.argv[1]

        config.mode = Mode.DEPLOYED
        if "-d" in sys.argv:
            config.mode = Mode.DEBUG
        super().__init__(role, config)
