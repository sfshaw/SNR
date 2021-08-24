
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class TimerProtocol(Protocol):

    def current_s(self) -> float:
        ...
