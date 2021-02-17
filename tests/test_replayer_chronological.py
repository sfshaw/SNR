import logging
import pytest

from snr import *


class TestReplayerChronological(SNRTestCase):

    @pytest.mark.timeout(1000)
    def test_replayer_chronological(self):

        with self.ordered_expector([
            (TaskType.process_data, "raw_data1"),
            (TaskType.process_data, "raw_data2"),
            (TaskType.process_data, "raw_data3"),
            (TaskType.process_data, "raw_data4"),
        ]) as ordered_expector:

            with self.temp_file("input.tmp") as input, \
                    self.temp_file("output.tmp") as output:

                expected_pages = [
                    Page("raw_data1", "data1", "test_node", 0.010),
                    Page("raw_data2", "data2", "test_node", 0.020),
                    Page("raw_data3", "data3", "test_node", 0.030),
                    Page("raw_data4", "data4", "test_node", 0.040),
                ]

                with input.open() as f:
                    for page in expected_pages:
                        f.write(page.serialize() + "\n")
                input.assertExists()

                times: List[float] = []

                self.run_test_node([
                    ReplayerFactory(input.path,
                                    exit=True),
                    RecorderFactory(output.path,
                                    ["raw_data1",
                                     "raw_data2",
                                     "raw_data3",
                                     "raw_data4",
                                     "raw_data5"]),
                    StopwatchEndpointFactory(times),
                    ExpectorEndpointFactory(ordered_expector),
                ])

                time_diffs: List[float] = []
                for i in range(len(times) - 1):
                    time_diffs.append(times[i + 1] - times[i])
                avg = sum(time_diffs)/len(time_diffs)
                self.assertGreater(avg, 0.005)
                self.assertGreater(0.015, avg)

                output.assertExists()
                with open(output.path) as f:
                    actual_pages = [Page.deserialize(f.readline())
                                    for _ in range(len(expected_pages))]
                    logging.getLogger("Page").setLevel(
                        logging.CRITICAL)  # Supress error
                    self.assertIsNone(Page.deserialize(f.readline()))
                    self.assertEqual(expected_pages, actual_pages)


if __name__ == '__main__':
    unittest.main()
