from snr_core.endpoint.endpoint import EndpointBase
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_std.io.replayer import raw_data_replayer
from snr_core.node import Node


class RawDataReplayerFactory(EndpointFactory):
    def __init__(self,
                 input_filename: str,
                 output_data_name: str,
                 exit: bool = False
                 ) -> None:
        super().__init__("Raw Data Replayer Factory")
        self.input_filename = input_filename
        self.output_data_name = output_data_name
        self.exit = exit

    def get(self, parent: Node) -> EndpointBase:
        return raw_data_replayer.RawDataReplayer(self,
                                                 parent,
                                                 self.input_filename,
                                                 self.output_data_name,
                                                 self.exit)
