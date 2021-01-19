from snr_core.endpoint.endpoint import Endpoint
from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.node import Node

import snr.comms.serial_conn.serial_connection


class SerialConnectionFactory(EndpointFactory):
    def __init__(self, transmit_data_name: str, query_data_name: str,
                 firmware_path: str):
        super().__init__("Serial Connection Factory")
        self.transmit_data_name = transmit_data_name
        self.query_data_name = query_data_name
        # TODO: Support updating Arduino firmware on startup
        self.firmware_path = firmware_path

    def get(self, parent: Node) -> Endpoint:
        return serial_connection.SerialConnection(parent,
                                                  "Serial Connection",
                                                  self.transmit_data_name,
                                                  self.query_data_name)
