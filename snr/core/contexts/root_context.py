import logging
from typing import Optional, Union

from snr.interfaces import *
from snr.interfaces.abstract_context import LOG_LEVELS
from snr.type_defs import *

from ..core_utils import Timer
from .context import Context

LOG_FORMAT = "[%(name)s:\t%(levelname)s]\t%(message)s\t"


class RootContext(Context):

    def __init__(self,
                 name: str,
                 mode: Union[Mode, LogLevel],
                 profiler: Optional[AbstractProfiler] = None,
                 ) -> None:
        logging.basicConfig(format=LOG_FORMAT)
        super().__init__(name, profiler, Timer())
        if isinstance(mode, Mode):
            level = LOG_LEVELS[mode]
        else:
            level = mode
        self.log.setLevel(level)

    def terminate_context(self) -> None:
        if self.profiler:
            self.profiler.join_from("terminate_root_context")
            self.info(self.profiler.dump())
