from snr.core.base import *

from . import video_receiver, video_source
from .camera_config import CameraConfig


class VideoSourceFactory(LoopFactory):
    def __init__(self, config: CameraConfig):
        super().__init__("Video Source Factory", video_source)
        self.config = config

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        ip: Optional[str] = parent.get_data("node_ip_address")
        if not ip:
            raise Exception("Node ip address not found in datastore")
        return video_source.VideoSource(self,
                                        parent,
                                        f"{self.config.name} source",
                                        ip,
                                        self.config.server_port,
                                        self.config.camera_num)

    def __repr__(self):
        return "Video(Cam: {}) Source Factory:{}".format(
            self.config.camera_num,
            self.config.server_port
        )


class VideoReceiverFactory(LoopFactory):
    def __init__(self, config: CameraConfig) -> None:
        super().__init__("Video Receiver Factory", video_receiver)
        self.config = config

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        return video_receiver.VideoReceiver(self,
                                            parent,
                                            f"{self.config.name} receiver",
                                            self.config.server_port)

    def __repr__(self):
        return f"Video Receiver Factory: {self.config.name}"


class CameraPair:
    def __init__(self, config: CameraConfig):
        self.config = config

        self.source = VideoSourceFactory(self.config)
        self.receiver = VideoReceiverFactory(self.config)
