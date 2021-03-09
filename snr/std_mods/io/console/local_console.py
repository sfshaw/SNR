from typing import List, Optional

from .remote_console import RemoteConsole


class LocalConsole(RemoteConsole):
    def __init__(self,
                 server_port: int,
                 commands: Optional[List[str]] = None,
                 retry_wait_s: float = 0.5
                 ) -> None:
        super().__init__(("localhost", server_port),
                         commands,
                         retry_wait_s=retry_wait_s,
                         name="local_console")
