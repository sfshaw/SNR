import sys

import snr

from control_processor_factory import ControlProcessorFactory
from controller_loop_factory import ControllerLoopFactory
from input_mapping_factory import InputMappingFactory

raw_controller_data = "raw_controller_data"
controller_data = "controller_data"


sockets = snr.SocketsPair(server_tuple=("localhost", 9000))

components: snr.ComponentsByRole = {
    "input_device": [
        ControllerLoopFactory(raw_controller_data),
        InputMappingFactory(raw_controller_data, controller_data),
        snr.PrinterEndpointFactory([
            (snr.TaskType.event, "button_pressed"),
            (snr.TaskType.event, "button_released"),
        ]),
        sockets.client([controller_data]),
        snr.TimeoutLoopFactory(seconds=20),
    ],
    "receiver": [
        sockets.server(),
        ControlProcessorFactory(controller_data),
        snr.PrinterEndpointFactory([
            (snr.TaskType.event, "button_pressed"),
            (snr.TaskType.event, "button_released"),
        ])
    ]
}

if __name__ == '__main__':
    snr.CliRunner(components, sys.argv).run()
