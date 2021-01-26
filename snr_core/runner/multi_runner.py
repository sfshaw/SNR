from typing import Dict, List

from snr_core.config import Mode
from snr_core.factory.factory_base import FactoryBase
from snr_core.runner import Runner


class MultiRunner(Runner):

    def __init__(self,
                 mode: Mode,
                 factories_by_role: Dict[str, List[FactoryBase]] = {}
                 ) -> None:
        self.mode = mode
        self.factories_by_role = factories_by_role
