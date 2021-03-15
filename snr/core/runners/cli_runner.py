import sys
from typing import List

from snr.interfaces import *
from snr.type_defs import *

from ..config import Config
from .synchronous_runner import SynchronousRunner


class CliRunner(SynchronousRunner):

    def __init__(self,
                 components: ComponentsByRole,
                 argv: List[str] = sys.argv,
                 ) -> None:
        argc = len(argv)
        if argc < 2:
            print(f"usage: {sys.executable} {argv[0]} [node role]")
            sys.exit(1)
        role = argv[1]

        mode = Mode.DEPLOYED
        if "-d" in argv:
            mode = Mode.DEBUG
        super().__init__(role, Config(mode, components))
