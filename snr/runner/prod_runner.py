import sys

from snr.config import Config, Mode
from snr.runner.synchronus_runner import SynchronousRunner
from snr.utils.utils import print_usage


class ProdRunner(SynchronousRunner):

    def __init__(self, config: Config):
        argc = len(sys.argv)
        if argc < 2:
            print_usage()
            sys.exit(1)
        role = sys.argv[1]

        mode: Mode = Mode.DEPLOYED
        if "-d" in sys.argv:
            mode = Mode.DEBUG
        super(SynchronousRunner).__init__(mode, role, config)
