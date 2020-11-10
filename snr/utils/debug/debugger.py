from enum import Enum
from sys import stdin
from typing import Any, List, Union

from snr.settings import Settings
from snr.utils.consumer import Consumer
from snr.utils.utils import format_message

SLEEP_TIME_S = 0.025
# 5 ms => 200 Hz cap on debug messages being printed
# 10 ms => 100 Hz cap
# 33 ms => 30 Hz cap


class PromptState(Enum):
    NotRequested = 0
    Requested = 1
    Completed = 2


class Debugger(Consumer):
    """Print debugging framework allowing any thread or process to send lines
    to be printed on stdout. Channels can be used to filter which messages are
    printed. Messages can be formatted.
    """

    def __init__(self, settings: Settings) -> None:
        super().__init__("debugger",
                         self.prompt_or_print,
                         SLEEP_TIME_S)
        self.settings = settings
        self.prompt_state: PromptState = PromptState.NotRequested
        self.prompt_message: str = ""

    def prompt_or_print(self, data: str) -> None:
        if self.prompt_state is PromptState.Requested:
            print(self.prompt_message)
            self.prompt_message = stdin.readline()
            self.prompt_state = PromptState.Completed
        print(data)

    def prompt(self, prompt_message: str) -> str:
        '''Called from outside the debugger thread
        '''
        if self.prompt_state is PromptState.Requested:
            print("Waiting for previous propmt to complete")
            self.catch_up("Prompt")
        self.prompt_message = prompt_message
        self.prompt_state = PromptState.Requested
        print("Prompt requested")
        self.catch_up("Waiting for prompt")
        while self.prompt_state is not PromptState.Completed \
                and not self.prompt_message:
            self.catch_up("Still waiting for prompt")
        return self.prompt_message

    def debug(self,
              context_name: str,
              level: str,
              message: str,
              format_args: Union[List[Any], Any, None] = None):
        channel = f"{context_name}_{level}"
        settings = self.settings
        channel_active = settings.DEBUG_CHANNELS.get(channel) is not False
        # TODO: Use settings.ROLE for per client and server debugging?
        if(settings.DEBUG_PRINTING and channel_active):
            self.__queue_message(
                format_message(context_name, level, message, format_args))
        if (settings.DEBUG_LOGGING
                and ()):
            # TODO: Output stuff to a log file
            pass

    def __queue_message(self, s: str):
        self.put(s)
        # print(s)
