# from snr.core import *
# from snr.interfaces import *
# from snr.type_defs import *


# class KalmanEndpoint(Endpoint):
#     def __init__(self,
#                  factory: EndpointFactory,
#                  parent: AbstractNode,
#                  name: ComponentName,
#                  input_data_key: DataKey,
#                  output_data_key: DataKey
#                  ) -> None:
#         super().__init__(factory,
#                          parent,
#                          name)
#         self.task_handlers = {
#             (TaskType.store_page, input_data_key):
#             self.filter
#         }
#         self.input_data_key = input_data_key
#         self.output_data_key = output_data_key

#     def task_source(self) -> None:
#         return None

#     def filter(self, t: Task, k: TaskId) -> SomeTasks:
#         assert isinstance(t.val_list[0], Page) and \
#             isinstance(t.val_list[0].data, str)
#         input = t.val_list[0].data
#         # TODO: Use Kalman filter implementation
#         output: str = input  # No op
#         return self.task_store_data(self.output_data_key, output)

#     def begin(self) -> None:
#         pass

#     def halt(self) -> None:
#         pass

#     def terminate(self) -> None:
#         pass
