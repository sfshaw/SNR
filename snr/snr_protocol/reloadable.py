from snr.snr_types import *

from .component_protocol import ComponentProtocol
from .factory_protocol import FactoryProtocol


@runtime_checkable
class Reloadable(ComponentProtocol, Protocol):
    factory: FactoryProtocol

    def reload(self) -> None:
        self.factory.reload()
        self.join()
