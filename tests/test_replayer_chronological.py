import logging
from typing import List

import pytest
from snr import *


class TestReplayerChronological(SNRTestCase):

    @pytest.mark.timeout(0.750)
    def test_replayer_chronological(self):

        time_step_s: float = 0.025

        with self.ordered_expector([
            (TaskType.store_page, "raw_data1"),
            (TaskType.store_page, "raw_data2"),
            (TaskType.store_page, "raw_data3"),
            (TaskType.store_page, "raw_data4"),
            (TaskType.store_page, "raw_data5"),
        ]) as ordered_expector:

            with self.temp_file("input.tmp") as input, \
                    self.temp_file("output.tmp") as output:

                expected_pages = [
                    Page("raw_data1", "data1", "test_node", time_step_s),
                    Page("raw_data2", "data2", "test_node", time_step_s * 2),
                    Page("raw_data3", "data3", "test_node", time_step_s * 3),
                    Page("raw_data4", "data4", "test_node", time_step_s * 4),
                    Page("raw_data5", "data5", "test_node", time_step_s * 5),
                ]

                with input.open() as f:
                    for page in expected_pages:
                        f.write(page.serialize().decode())
                        f.write("\n")
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

                self.assertEqual(times, sorted(times))
                time_diffs: List[float] = []
                for i in range(len(times) - 1):
                    time_diffs.append(times[i + 1] - times[i])
                avg = sum(time_diffs)/len(time_diffs)
                self.assertGreater(avg, time_step_s / 2)
                self.assertLess(avg, time_step_s * 2)

                output.assertExists()
                with open(output.path) as f:
                    actual_pages = [Page.deserialize(f.readline())
                                    for _ in range(len(expected_pages))]
                    logging.getLogger("Page").setLevel(
                        logging.CRITICAL)  # Supress error
                    self.assertIsNone(Page.deserialize(f.readline()))
                    self.assertEqual(expected_pages, actual_pages)
