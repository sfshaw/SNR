from snr import *


class TestMovingAvgEndpoint(SNRTestCase):

    def test_moving_avg_endpoint(self):
        input_data = "input_data"
        output_data = "filtered_Data"

        expectations = {
            (TaskType.store_page, input_data): 4,
            (TaskType.process_data, input_data): 4,
            (TaskType.store_page, output_data): 4,
            (TaskType.process_data, output_data): 4,
        }
        with self.expector(expectations) as expector:
            self.run_test_node([
                ListReplayerFactory([0, 1, 2, 4], input_data),
                MovingAvgFilterFactory(input_data, output_data, 2),
                ExpectorEndpointFactory(expector, exit_when_satisfied=True)
            ])
