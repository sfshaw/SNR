from snr.types.base import *


class SocketsConfig:
    def __init__(self,
                 ip: str,
                 port: int):
        self.ip = ip
        self.port = port
        self.required: bool = True

    def tuple(self) -> Tuple[str, int]:
        return self.ip, self.port
