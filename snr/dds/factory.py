
from snr.factory import Factory
from typing import List

from snr.dds.dds_connection import DDSConnection


class DDSFactory(Factory):
    def __init__(self):
        pass

    def get(self,
            parent_node,
            parent_dds
            ) -> List[DDSConnection]:
        raise NotImplementedError
