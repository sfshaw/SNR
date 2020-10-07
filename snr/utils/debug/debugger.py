from queue import Empty
from snr.utils.utils import format_message
from snr.utils.consumer import Consumer
from time import sleep
from typing import List, Union, Callable


from snr.settings import Settings

SLEEP_TIME_S = 0.025
# 5 ms => 200 Hz cap on debug messages being printed
# 10 ms => 100 Hz cap
# 33 ms => 30 Hz cap


class Debugger(Consumer):
    """Print debugging framework allowing any thread or process to send lines
    to be printed on stdout. Channels can be used to filter which messages are
    printed. Messages can be formatted.
    """

    def __init__(self, settings: Settings):
        super().__init__("debugger",
                         print,
                         SLEEP_TIME_S)
        self.settings = settings

    def debug(self, context_name: str, level: str, *args: Union[List,  str]):
        """Debugging print and logging function

        Records information for debugging by printing or logging to disk.
            args is a list of arguments to be formatted. Various channels
            can be toggled on or off from settings.DEBUG_CHANNELS dict.
            Channels not found in the dict while be printed by default.

        Usage:
        // In constructor
        self.dbg = debug  // localize parameter for ease of use

        // later
        self.dbg("channel", "message")
        self.dbg("channel", object)
        self.dbg("channel",
                 "message: {}, {}",
                 ["list", thing_to_format]) // Respect line limit

        respective outputs:
        [channel]   message
        [channel]   object.__repr__()
        [channel]   message with brackets: list, thing_to_format.__repr__()

        By formatting once inside debug(), format() is only called if
        printing is turned on. Remember to include [ ] around the items
        to be formatted.

        A single thread handles all calls by consuming a Queue.
        """
        channel = f"{context_name}_{level}"
        settings = self.settings
        channel_active = settings.DEBUG_CHANNELS.get(channel) is not False
        # TODO: Use settings.ROLE for per client and server debugging?
        if(settings.DEBUG_PRINTING and channel_active):
            self.__queue_message(
                format_message(context_name, level, *args))
        if (settings.DEBUG_LOGGING
                and ()):
            # TODO: Output stuff to a log file
            pass

    def __queue_message(self, s: str):
        self.put(s)
        # print(s)
