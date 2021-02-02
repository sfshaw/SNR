import sys

from snr.snr_core.config import Config, Mode
from snr.snr_core.utils.utils import print_usage
from snr.snr_types import *

from .synchronus_runner import SynchronousRunner


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
