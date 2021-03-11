from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .context_protocol import ContextProtocol


@runtime_checkable
class ComponentProtocol(ContextProtocol, Protocol):

    def begin(self) -> None:
        ...

    def join(self) -> None:
        ...

    def terminate(self) -> None:
        ...
