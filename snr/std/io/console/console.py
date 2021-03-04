import io
import socket
import sys
import threading

from snr.core.base import *
from snr.core.context.root_context import RootContext
from snr.core.utils.sockets.sockets_wrapper import SocketsWrapper

PROMPT = "> "


class RemoteConsole(threading.Thread):
    def __init__(self,
                 server_tuple: Tuple[str, int],
                 commands: Optional[List[str]] = None,
                 retry_wait_s: float = 0.5
                 ) -> None:
        super().__init__(target=self.thread_fn,
                         name="console_thread",
                         daemon=False)
        self.root_context = RootContext("remote_console", None, Settings())
        self.server_tuple = server_tuple
        self.retry_wait_s = retry_wait_s
        self.input_file = sys.stdin
        if commands:
            self.input_file = io.StringIO("\n".join(commands) + "\n")
        self.prompt_text: str = server_tuple[0] + PROMPT
        # self.commands: Dict[str, Command] = {
        #     "exit": self.cmd_exit,
        #     "task": self.cmd_schedule_task,
        #     "reload": self.cmd_reload,
        #     "list": self.cmd_list,
        # }
        self.__terminate_flag = threading.Event()
        self.connection = SocketsWrapper(
            (socket.create_connection(self.server_tuple),
             self.server_tuple),
            self.root_context)
        self.start()

    def thread_fn(self) -> None:
        with self.connection as _:
            while not self.is_terminated():
                input = self.get_input()
                if input:
                    self.handle_input(input)
                else:
                    self.set_terminate_flag()

    def get_input(self) -> Optional[str]:
        sys.stdout.write(self.prompt_text)
        sys.stdout.flush()
        input: Optional[str] = None
        try:
            input = self.input_file.readline().rstrip()
            if self.input_file is not sys.stdin:
                sys.stdout.write(input)
                sys.stdout.flush()
        except EOFError:
            self.set_terminate_flag()
        return input

    def handle_input(self, input: str):
        page = Page("console_cmd", input, self.name, 0)
        self.connection.send(page.serialize())
        if input == "exit":
            self.set_terminate_flag()

    def is_terminated(self) -> bool:
        return self.__terminate_flag.is_set()

    def set_terminate_flag(self):
        self.__terminate_flag.set()

    def join(self, timeout: Optional[float] = None):
        self.set_terminate_flag()
        super().join(timeout)


class LocalConsole(RemoteConsole):
    def __init__(self,
                 server_port: int,
                 commands: Optional[List[str]] = None,
                 retry_wait_s: float = 0.5
                 ) -> None:
        super().__init__(("localhost", server_port),
                         commands,
                         retry_wait_s=retry_wait_s)


if __name__ == "__main__":
    LocalConsole(54321)
