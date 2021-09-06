import snr
from controller_loop_factory import ControllerLoopFactory

components: snr.ComponentsByRole = {
    "test": [
        snr.TimeoutLoopFactory(seconds=20),
        ControllerLoopFactory(),
    ]
}

if __name__ == '__main__':
    snr.CliRunner(components).run()
