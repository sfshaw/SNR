import io
import logging
import socket
import sys
import threading
from typing import List, Optional, Tuple

from snr.core import *
from snr.prelude import *

from ...comms import SocketsWrapper

DEFAULT_PORT: int = 54321

PROMPT = "> "
COMMAND_DATA_NAME: str = "console_command"
COMMAND_ACK_DATA_NAME: str = "console_command_response"
POLL_TIMEOUT: float = 0.500


class RemoteConsole(RootContext):
    def __init__(self,
                 server_tuple: Tuple[str, int],
                 commands: Optional[List[str]] = None,
                 retry_wait_s: float = 0.5,
                 name: str = "remote_console",
                 ) -> None:
        super().__init__(name, logging.INFO)
        self.server_tuple = server_tuple
        self.retry_wait_s = retry_wait_s
        self.input_file = sys.stdin
        if commands:
            self.input_file = io.StringIO("\n".join(commands) + "\n")
        self.prompt_text: str = server_tuple[0] + PROMPT
        self.__terminate_flag = threading.Event()
        self.connection = SocketsWrapper(
            (socket.create_connection(self.server_tuple),
             self.server_tuple),
            self)
        self.connection.open()
        sys.stdout.write("Connected to {}:{}\n".format(
                         self.server_tuple[0],
                         self.server_tuple[1]))

    def run(self) -> None:
        try:
            with self.connection:
                while not self.is_terminated():
                    input = self.get_input()
                    if input:
                        self.handle_input(input)
                        self.handle_response()
                    else:
                        self.set_terminate_flag()
                    sys.stdout.write("\n")
                    sys.stdout.flush()
        except KeyboardInterrupt:
            sys.exit(0)

    def get_input(self) -> Optional[str]:
        sys.stdout.write(self.prompt_text)
        sys.stdout.flush()
        input: Optional[str] = None
        try:
            input = self.input_file.readline()
            if self.input_file is not sys.stdin:
                sys.stdout.write(input)
                sys.stdout.flush()
        except EOFError:
            self.set_terminate_flag()
        return input

    def handle_input(self, input: str) -> None:
        self.dbg("Handling input: %s", input.encode())
        if len(input):
            args = input.rstrip().split(" ")
            page = Page(COMMAND_DATA_NAME,
                        args,
                        self.name,
                        0)
            self.connection.send(page.serialize())
        if input == "exit" or input == "":
            self.set_terminate_flag()

    def handle_response(self) -> None:
        # if self.connection.poll(0):
        response = self.connection.recv()
        if response:
            page = Page.deserialize(response)
            if page:
                sys.stdout.write(page.data)
                sys.stdout.flush()
            else:
                self.warn("Could not deserialize page")
                self.set_terminate_flag()
        else:
            sys.stdout.write("\nDisconnected\n")
            self.set_terminate_flag()
        # else:
        #     self.warn("Response timed out")

    def is_terminated(self) -> bool:
        return self.__terminate_flag.is_set()

    def set_terminate_flag(self):
        self.__terminate_flag.set()
