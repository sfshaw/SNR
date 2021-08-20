import logging
from typing import List

import pytest
from snr import *


class TestReplayer(SNRTestCase):

    @pytest.mark.timeout(1.000)
    def test_replayer(self):

        time_step_s: float = 0.020
        num_data_points = 5
        data_keys = [f"raw_data{i}" for i in range(1, num_data_points + 1)]
        expectations: List[TaskId] = []
        for key in data_keys:
            expectations.append((TaskType.store_data, key))

        expected_pages = [Page(key, key, "test_node", time_step_s * (i + 1))
                          for i, key in enumerate(data_keys)]

        times: List[float] = []

        with self.ordered_expector(expectations) as ordered_expector, \
                self.temp_file() as input, \
                self.temp_file() as output:

            with input.open() as f:
                for page in expected_pages:
                    f.write(page.serialize().decode())
                    f.write("\n")
            input.assertExists()

            self.run_test_node([
                ReplayerLoopFactory(input.path),
                RecorderEndpointFactory(output.path, data_keys),
                StopwatchEndpointFactory(times, [TaskType.store_data]),
                ExpectorEndpointFactory(ordered_expector,
                                        name="data_expector"),
                ExpectorEndpointFactory(self.expector({(TaskType.process_data,
                                                        data_keys[-1]): 1
                                                       }),
                                        name="completion_expector",
                                        exit_when_satisfied=True)
            ])

            # Check output file
            output.assertExists()
            with open(output.path) as f:
                actual_pages = [Page.deserialize(f.readline())
                                for _ in range(len(expected_pages))]
                logging.getLogger("Page").setLevel(
                    logging.CRITICAL)  # Supress error
                self.assertIsNone(Page.deserialize(f.readline()))
                self.assertEqual(expected_pages, actual_pages)

        # Check timing
        self.assertEqual(times, sorted(times))
        time_diffs = [times[i + 1] - times[i]
                      for i in range(len(times) - 1)]
        avg = sum(time_diffs) / len(time_diffs)
        msg = f"\nTimes: {times}\nTime diffs: {time_diffs}"
        self.assertAlmostEqual(avg, time_step_s,
                               delta=time_step_s / num_data_points,
                               msg=msg)
