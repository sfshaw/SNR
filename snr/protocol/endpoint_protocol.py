from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .handles_task import HandlesTasks
from .reloadable import Reloadable


@runtime_checkable
class EndpointProtocol(HandlesTasks, Reloadable, Protocol):

    def task_source(self) -> SomeTasks:
        ...

    def set_terminate_flag(self) -> None:
        ...

    def terminate(self) -> None:
        ...
