from snr import *
from snr_core.context.context import Context
from snr_core.context.root_context import RootContext
from snr_std.io.replayer.raw_data_replayer import RawReader

raw_data_filename = "tests/test_data/in/raw_data.txt"


class TestRawDataReplayer(SNRTestBase):

    def test_raw_reader(self):
        root = RootContext("test")
        context = Context("context", root)
        reader = RawReader(context, "test_reader", raw_data_filename)
        try:
            self.assertEqual("test_data", reader.read())
            self.assertIsNone(reader.read())
        finally:
            reader.close()

    def test_raw_data_replayer(self):
        with Expector(
            {
                (TaskType.process_data, "raw_data"): 1,
                TaskType.terminate: 1,
            },
                self) as expector:
            config: Config = self.get_config([
                RawDataReplayerFactory(raw_data_filename,
                                       "raw_data",
                                       exit=True),
                ExpectorEndpointFactory(expector)
            ],
                mode=Mode.DEBUG)
            runner = SynchronusTestRunner(config)
            runner.run()


if __name__ == '__main__':
    unittest.main()
