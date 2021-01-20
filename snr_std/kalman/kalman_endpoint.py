from snr_core.endpoint.endpoint_factory import EndpointFactory
from snr_core.endpoint.endpoint import Endpoint
from snr_core.node import Node
from snr_core.task import SomeTasks, Task, TaskId, TaskType


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
