from typing import Dict, List, Optional

from snr_core.base import *
from snr_std.camera.config import CameraConfig, ManagerRole
from snr_std.camera import manager, video_source, video_receiver


class VideoSourceFactory(EndpointFactory):
    def __init__(self, config: CameraConfig):
        super().__init__(manager, "Video Source Factory")
        self.config = config

    def get(self, parent_node: NodeProtocol) -> Endpoint:
        ip: Optional[str] = parent_node.get_data("node_ip_address")
        if not ip:
            raise Exception("Node ip address not found in datastore")
        return video_source.VideoSource(self,
                                        parent_node,
                                        f"{self.config.name} source",
                                        ip,
                                        self.config.server_port,
                                        self.config.camera_num)

    def __repr__(self):
        return f"Video(Cam: {self.config.camera_num}) Source Factory:{self.config.server_port}"


class VideoReceiverFactory(EndpointFactory):
    def __init__(self, config: CameraConfig) -> None:
        super().__init__(video_receiver, "Video Receiver Factory")
        self.config = config

    def get(self, parent_node: NodeProtocol) -> Endpoint:
        return video_receiver.VideoReceiver(self,
                                            parent_node,
                                            f"{self.config.name} receiver",
                                            self.config.server_port)

    def __repr__(self):
        return f"Video Receiver Factory: {self.config.name}"


class CameraPair:
    def __init__(self, config: CameraConfig):
        self.config = config

        self.source = VideoSourceFactory(self.config)
        self.receiver = VideoReceiverFactory(self.config)


class CameraManagerFactory(EndpointFactory):
    def __init__(self, role: ManagerRole, camera_names: List[str]):
        super().__init__(manager, "Camera Manager Factory")
        self.role = role
        self.camera_names = camera_names

    def get(self, parent: NodeProtocol) -> Endpoint:
        name_to_index: Dict[str, int] = {}
        i = 0
        for name in self.camera_names:
            name_to_index[name] = i
            i += 1
        return manager.CameraManager(self,
                                     parent,
                                     f"video_{self.role}_manager",
                                     self.role,
                                     name_to_index)

    def __repr__(self):
        return f"Camera Manager({self.role}) Factory"


class CameraManagerPair():
    def __init__(self, camera_names: List[str]):
        self.names = camera_names
        self.receiver = CameraManagerFactory(ManagerRole.Receiver,
                                             camera_names)
        self.source = CameraManagerFactory(ManagerRole.Source,
                                           camera_names)
