from __future__ import annotations

import logging

from snr_core.settings import Settings

LOG_FORMAT = "[%(name)s:\t%(levelname)s]\t%(message)s\t"
LOG_LEVEL = logging.WARNING


class RootContext:
    def __init__(self,
                 name: str,
                 ) -> None:
        self.name = name
        logging.basicConfig(format=LOG_FORMAT)
        self.log = logging.getLogger()
        self.settings = Settings()
