from snr.core import *
from snr.interfaces import *
from snr.type_defs import *


class KalmanEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 name: str,
                 input_data_name: str,
                 output_data_name: str
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name)
        self.task_handlers = {
            (TaskType.store_page, input_data_name):
            self.filter
        }
        self.input_data_name = input_data_name
        self.output_data_name = output_data_name

    def task_source(self) -> None:
        return None

    def filter(self, t: Task, k: TaskId) -> SomeTasks:
        assert isinstance(t.val_list[0], Page) and \
            isinstance(t.val_list[0].data, str)
        input = t.val_list[0].data
        # TODO: Use Kalman filter implementation
        output: str = input  # No op
        return self.task_store_data(self.output_data_name, output)

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
