'''This module defines loops, endpoints, and factories for receiving commands
 over a scoket. The remote console for sending commands from a terminal is
 also defined.
'''

from .local_console import LocalConsole
from .remote_console import DEFAULT_PORT, RemoteConsole

__all__ = [
    "DEFAULT_PORT",
    "RemoteConsole",
    "LocalConsole",
]
