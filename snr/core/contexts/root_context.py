import logging
from typing import Optional, Union

from snr.protocol import *
from snr.type_defs import *

from .context import Context

LOG_FORMAT = "[%(name)s:\t%(levelname)s]\t%(message)s\t"


class RootContext(Context):
    def __init__(self,
                 name: str,
                 mode: Union[Mode, LogLevel],
                 profiler: Optional[ProfilerProtocol] = None,
                 settings: Settings = Settings(),

                 ) -> None:
        self.profiler = profiler
        logging.basicConfig(format=LOG_FORMAT)
        self.log = logging.getLogger()
        if isinstance(mode, Mode):
            level = settings.log_level[mode]
        else:
            level = mode
        self.log.setLevel(level)
        super().__init__(name, settings, self.profiler)

    def terminate_context(self) -> None:
        if self.profiler:
            self.profiler.join_from("terminate_root_context")
            self.info(self.profiler.dump())
