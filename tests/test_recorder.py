import logging

from snr import *


class TestRecorder(SNRTestBase):

    def test_recorder_encoding(self):
        logging.getLogger("Page").setLevel(logging.WARN)
        with self.expector({(
            TaskType.process_data, "raw_data"): 1,
        }) as expector:

            with self.temp_file("raw_data_input.txt"
                                ) as input, \
                    self.temp_file("output.tmp") as output:

                with input.open() as f:
                    f.write("test_data\n")

                self.run_test_node([
                    TextReplayerFactory(input.path,
                                        "raw_data"),
                    RecorderFactory(output.path, ["raw_data"]),
                    ExpectorEndpointFactory(expector, exit_when_done=True)
                ])

                output.assertExists()
                with open(output.path) as f:
                    line = f.readline()
                    page = Page.deserialize(line)
                    if page:
                        self.assertEqual("raw_data", page.key)
                        self.assertEqual("test_data", page.data)
                        self.assertEqual("test_node", page.origin)
                    else:
                        self.log.error("Deserialization of %s failed, got %s",
                                       line, page)
                        self.assertTrue(False,
                                        f"Deserialization of page failed")


if __name__ == '__main__':
    unittest.main()
