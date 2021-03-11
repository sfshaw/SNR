from build.lib.snr.protocol.component_protocol import ComponentProtocol
from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .context_protocol import ContextProtocol
from .handles_task import HandlesTasks
from .reloadable import Reloadable


@runtime_checkable
class EndpointProtocol(ComponentProtocol, Reloadable, HandlesTasks, Protocol):

    def task_source(self) -> SomeTasks:
        ...

    def begin(self) -> None:
        ...

    def halt(self) -> None:
        ...

    def terminate(self) -> None:
        ...
