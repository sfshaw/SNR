import sys

import snr
import urov

controller_input_sockets = urov.SocketsPair(server="192.168.1.10:9000")
telemetry_sockets = urov.SocketsPair(server="192.168.1.11:9001")
components: snr.ComponentsByRole = {
    "control_unit": [
        # Topside control pipeline
        urov.XBoxControllerFactory("raw_controller_input"),
        urov.InputProcessorFactory("raw_controller_input",
                                   "controller_input"),
        controller_input_sockets.client_factory("controller_input"),
        # Topside sensor pipeline
        telemetry_sockets.server_factory(),
        urov.SensorDisplayEndpointFactory("sensor_data"),
    ],
    'urov': [
        # Robot control pipeline
        controller_input_sockets.server_factory(),
        urov.ControlsProcessorFactory("controller_input"),
        urov.MotorControllerFactory("motor_speed", "motor_data"),
        urov.SerialConnectionFactory("motor_data"),
        # On robot sensor pipeline
        urov.SensorsProcessorFactory("sensor_data"),
        controller_input_sockets.client_factory("sensor_data"),
    ],
}

if __name__ == "__main__":
    snr.CliRunner(components, sys.argv).run()
