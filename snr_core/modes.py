from enum import Enum
from typing import Callable, Dict, List

from snr_core.factory.factory_protocol import FactoryProtocol


class Mode(Enum):
    DEBUG = "debug"
    DEPLOYED = "deployed"
    TEST = "test"


Role = str
Components = List[FactoryProtocol]
ComponentsByRole = Dict[Role, Components]
ComponentsGetter = Callable[[Role], ComponentsByRole]
