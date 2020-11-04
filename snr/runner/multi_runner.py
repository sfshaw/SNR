from typing import Dict, List

from snr.config import Mode
from snr.factory import Factory
from snr.runner.runner import Runner


class MultiRunner(Runner):

    def __init__(self,
                 mode: Mode,
                 factories_by_role: Dict[str, List[Factory]] = {}
                 ) -> None:
        self.mode = mode
        self.factories_by_role = factories_by_role
