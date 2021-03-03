from snr.protocol import *
from snr.types import *

from .context import Context, logging

LOG_FORMAT = "[%(name)s:\t%(levelname)s]\t%(message)s\t"
LOG_LEVEL = logging.WARNING


class RootContext(Context):
    def __init__(self,
                 name: str,
                 profiler: Optional[ProfilerProtocol],
                 settings: Settings = Settings(),
                 ) -> None:
        self.profiler = profiler
        logging.basicConfig(format=LOG_FORMAT)
        self.log = logging.getLogger()
        super().__init__(name, settings, self.profiler)

    def terminate_context(self) -> None:
        if self.profiler:
            self.profiler.join_from("terminate_root_context")
            self.profiler.dump()

    def __enter__(self) -> "RootContext":
        return self

    def __exit__(self, *args: Any) -> None:
        self.terminate_context()
