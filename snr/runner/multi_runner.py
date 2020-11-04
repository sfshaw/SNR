from snr.runner.synchronus_runner import SynchronousRunner
from snr.factory import Factory
from typing import Dict, List
from snr.runner.runner import Runner


class MultiRunner(Runner):

    def __init__(self,
                 mode: str,
                 factories_by_role: Dict[str, List[Factory]] = {}
                 ) -> None:
        self.mode = mode
        self.factories_by_role = factories_by_role
