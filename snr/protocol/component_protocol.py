from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .context_protocol import ContextProtocol
from .tasks_protocols import ProvidesTaskHandlers, ProvidesTasks
from .factory_protocol import FactoryProtocol


@runtime_checkable
class ComponentProtocol(ContextProtocol,
                        ProvidesTaskHandlers,
                        ProvidesTasks,
                        Protocol):
    factory: FactoryProtocol

    def begin(self) -> None:
        ...

    def join(self) -> None:
        ...

    def halt(self) -> None:
        ...

    def terminate(self) -> None:
        ...

    def schedule(self, t: SomeTasks) -> None:
        ...
