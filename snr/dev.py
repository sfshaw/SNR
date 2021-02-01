from snr import *


def main():
    CONSOLE_PORT: int = 54321
    runner = SynchronusTestRunner(
        Config(Mode.TEST,
               {"test": [
                CommandReceiverFactory(CONSOLE_PORT),
                CommandProcessorFactory()
                ]}))
    runner.run()


if __name__ == '__main__':
    main()
