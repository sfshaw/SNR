import sys

from snr.protocol import *
from snr.types import *

from .synchronus_runner import SynchronousRunner


class CLIRunner(SynchronousRunner):

    def __init__(self, config: ConfigProtocol):
        argc = len(sys.argv)
        if argc < 2:
            print(f"usage: {sys.executable} main.py [node role]")
            sys.exit(1)
        role = sys.argv[1]

        config.mode = Mode.DEPLOYED
        if "-d" in sys.argv:
            config.mode = Mode.DEBUG
        super().__init__(role, config)
