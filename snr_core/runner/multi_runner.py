from typing import Dict, List

from snr_core.config import Mode
from snr_core.endpoint.factory import Factory
from snr_core.runner import Runner


class MultiRunner(Runner):

    def __init__(self,
                 mode: Mode,
                 factories_by_role: Dict[str, List[Factory]] = {}
                 ) -> None:
        self.mode = mode
        self.factories_by_role = factories_by_role
