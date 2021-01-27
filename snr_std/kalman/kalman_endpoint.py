
from snr_core.base import *


class KalmanEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: Node,
                 name: str,
                 input_data_name: str,
                 output_data_name: str
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name,
                         task_handlers={
                             (TaskType.process_data, input_data_name):
                             self.filter
                         })
        self.input_data_name = input_data_name
        self.output_data_name = output_data_name

    def filter(self, t: Task, k: TaskId) -> SomeTasks:
        input = self.parent.get_data(self.input_data_name)
        output = input  # No op
        self.parent.store_data(self.output_data_name, output)
        return None
