# from typing import Dict, List
# from snr.core import *
# from snr.prelude import *

# from snr.std_mods.camera import manager
# from snr.std_mods.camera.camera_config import ManagerRole


# class CameraManagerFactory(LoopFactory):
#     def __init__(self, role: ManagerRole, camera_names: List[str]):
#         super().__init__(manager)
#         self.role = role
#         self.camera_names = camera_names

#     def get(self, parent: NodeProtocol) -> AbstractLoop:
#         name_to_index: Dict[str, int] = {}
#         i = 0
#         for name in self.camera_names:
#             name_to_index[name] = i
#             i += 1
#         return manager.CameraManager(self,
#                                      parent,
#                                      f"video_{self.role}_manager",
#                                      self.role,
#                                      name_to_index)

#     def __repr__(self):
#         return f"Camera Manager({self.role}) Factory"


# class CameraManagerPair():
#     def __init__(self, camera_names: List[str]):
#         self.names = camera_names
#         self.receiver = CameraManagerFactory(ManagerRole.Receiver,
#                                              camera_names)
#         self.source = CameraManagerFactory(ManagerRole.Source,
#                                            camera_names)
