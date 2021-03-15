from snr import *
from snr.std_mods.io.console import DEFAULT_PORT


class TestConsole(SNRTestCase):

    def test_console_fails_to_connect(self):
        commands = [
            "list endpoints",
            "exit"
        ]

        def try_console():
            LocalConsole(DEFAULT_PORT,
                         commands,
                         retry_wait_s=0.001)
            # Console constructor should block and raise

        self.assertRaises(ConnectionRefusedError, try_console)
