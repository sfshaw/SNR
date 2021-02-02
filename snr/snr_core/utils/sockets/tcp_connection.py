import pickle
import socket
import struct
import time
from socket import socket as Socket

from snr.snr_types.base import *

MAX_RETRIES = 10
RETRY_WAIT_S = 0.5

T = TypeVar("T")


class TCPConnection(Generic[T]):
    def __init__(self,
                 server_tuple: Tuple[str, int],
                 tries: int = MAX_RETRIES,
                 retry_wait_s: float = RETRY_WAIT_S
                 ) -> None:

        self.inner: Socket
        self.retry_wait_s = retry_wait_s
        while tries > 0:
            try:
                self.inner = Socket(socket.AF_INET, socket.SOCK_STREAM)
                self.inner.connect(server_tuple)
                return
            except Exception as e:
                self.inner.close()
                tries -= 1
                if not tries > 0:
                    raise e
                else:
                    time.sleep(self.retry_wait_s)

    def send(self, data: T) -> None:
        encoded_data = pickle.dumps(data)
        self.inner.send(struct.pack("I", len(encoded_data)))
        self.inner.send(encoded_data)

    def is_alive(self) -> bool:
        return self.inner is not None

    def __enter__(self) -> "TCPConnection[T]":
        return self

    def __exit__(self, *args: Any):
        self.inner.close()
