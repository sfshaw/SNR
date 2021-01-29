import pickle
import struct
from socket import AF_INET, SOCK_STREAM
from socket import socket as Socket
from time import sleep
from typing import Any, Generic, Tuple, TypeVar

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
                self.inner = Socket(AF_INET, SOCK_STREAM)
                self.inner.connect(server_tuple)
                return
            except Exception as e:
                self.inner.close()
                tries -= 1
                if not tries > 0:
                    raise e
                else:
                    sleep(self.retry_wait_s)

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
