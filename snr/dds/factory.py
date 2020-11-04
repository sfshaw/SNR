from typing import Any, List

from snr.dds.dds_connection import DDSConnection
from snr.factory import Factory


class DDSFactory(Factory):
    def __init__(self):
        pass

    def get(self,
            parent_node: Any,
            parent_dds: Any
            ) -> List[DDSConnection]:
        raise NotImplementedError
