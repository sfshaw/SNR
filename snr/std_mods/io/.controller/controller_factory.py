# from snr.core import *
# from snr.prelude import *

# from . import controller


# class ControllerFactory(LoopFactory):
#     def __init__(self, output_data_name: str):
#         super().__init__()
#         self.output_data_name = output_data_name

#     def get(self, parent: AbstractNode) -> ThreadLoop:
#         return controller.Controller(self,
#                                      parent,
#                                      self.output_data_name)
