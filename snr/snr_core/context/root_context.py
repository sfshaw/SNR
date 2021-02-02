import logging

from snr.snr_protocol import *
from snr.snr_types import *

LOG_FORMAT = "[%(name)s:\t%(levelname)s]\t%(message)s\t"
LOG_LEVEL = logging.WARNING


class RootContext(ContextProtocol):
    def __init__(self,
                 name: str,
                 ) -> None:
        self.name = name
        self.profiler = None
        logging.basicConfig(format=LOG_FORMAT)
        self.log = logging.getLogger()
        self.settings = Settings()
