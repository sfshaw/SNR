from snr import *


class TestConsole(SNRTestBase):

    def test_console_fails_to_connect(self):
        CONSOLE_PORT: int = 54321

        commands = [
            "list endpoints",
            "exit"
        ]

        def try_console():
            console = LocalConsole(CONSOLE_PORT,
                                   commands,
                                   retry_wait_s=0.001)
            # Console constructor blocks
            console.join()

        self.assertRaises(ConnectionRefusedError, try_console)
        # config = self.get_config([
        #     CommandReceiverFactory(CONSOLE_PORT),
        #     CommandProcessorFactory()])
        # runner = SynchronusTestRunner(config)
        # runner.run()
    pass


if __name__ == '__main__':
    unittest.main()
