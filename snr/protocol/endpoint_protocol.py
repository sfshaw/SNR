from snr.types import *

from .handles_task import HandlesTasks
from .reloadable import Reloadable


@runtime_checkable
class EndpointProtocol(HandlesTasks, Reloadable, Protocol):

    def task_source(self) -> SomeTasks:
        ...

    def set_terminate_flag(self) -> None:
        ...
