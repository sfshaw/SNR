
from enum import Enum


class CameraConfig:
    def __init__(self, name: str, server_port: int, camera_num: int):
        self.name = name
        self.server_port = server_port
        self.camera_num = camera_num


class ManagerRole(Enum):
    Source = 0
    Receiver = 1

    def as_str(self):
        if (self is ManagerRole.Source):
            return "source"
        else:
            return "receiver"
