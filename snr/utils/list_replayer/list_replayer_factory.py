from typing import Any, List

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from . import list_replayer_endpoint


class ListReplayerFactory(EndpointFactory):
    def __init__(self,
                 data: List[Any],
                 data_key: DataKey,
                 exit_when_done: bool = False,
                 ) -> None:
        super().__init__(list_replayer_endpoint)
        self.data = data
        self.data_key = data_key
        self.exit_when_done = exit_when_done

    def get(self, parent: AbstractNode) -> Endpoint:
        return list_replayer_endpoint.ListReplayerEndpoint(self,
                                                           parent,
                                                           self.data,
                                                           self.data_key,
                                                           self.exit_when_done)
