import logging
from typing import Optional

from snr import *
from snr.std_mods.io.recorder.recorder_endpoint import RecorderEndpoint


class TestRecorder(SNRTestCase):

    def test_invalid_task(self):
        with self.temp_file() as f:
            recorder: Optional[RecorderEndpoint] = None
            try:
                data_keys = ["data_key"]
                recorder = RecorderEndpoint(RecorderEndpointFactory(f.path,
                                                                    data_keys),
                                            self.mock_node(),
                                            "test_recorder",
                                            f.path,
                                            data_keys)
                recorder.log.setLevel(logging.WARNING)

                self.assertIsNone(recorder.task_handler(
                    Task(TaskType.process_data, "boring_data"),
                    (TaskType.process_data,
                     "totally invalid")))

                self.assertIsNone(recorder.task_handler(
                    tasks.event("boring_event"),
                    (TaskType.process_data, "totally invalid")))

                self.assertIsNone(recorder.task_handler(
                    Task(TaskType.process_data, "data_key"),
                    (TaskType.process_data, "data_key")))
            finally:
                if recorder:
                    recorder.join()
                    recorder.terminate()

    def test_recorder_encoding(self):
        with self.expector({
            (TaskType.process_data, "raw_data"): 1,
        }) as expector:

            with self.temp_file() as input, self.temp_file() as output:

                with input.open() as f:
                    f.write("test_data\n")

                self.run_test_node([
                    TextReplayerFactory(input.path,
                                        "raw_data"),
                    RecorderEndpointFactory(output.path, ["raw_data"]),
                    ExpectorEndpointFactory(expector, exit_when_satisfied=True)
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
                        logging.getLogger(self.test_name).error(
                            "Deserialization of %s failed, got %s", line, page)
                        self.assertTrue(False,
                                        "Deserialization of page failed")
