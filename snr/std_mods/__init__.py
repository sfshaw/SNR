'''This module provides a number of pre-made Endpoints and Loops for easy
 re-use. They should be imported via `snr` using `from snr import *`.

Some other classes may be available for additional imports.
'''

from snr.std_mods.comms import (CommsLoop, SocketsListenerFactory,
                                SocketsLoopFactory, SocketsWrapper)

from .comms.pipe.pipe_loop_factory import PipeLoopFactory
from .io.console.command_processor_factory import CommandProcessorFactory
from .io.console.command_receiver_factory import CommandReceiverFactory
from .io.console.console import LocalConsole, RemoteConsole
from .io.recorder.recorder_factory import RecorderFactory
from .io.replayer.page_reader import PageReader
from .io.replayer.replayer_factory import ReplayerFactory
from .io.replayer.text_reader import TextReader
from .io.replayer.text_replayer_factory import TextReplayerFactory
from .kalman.kalman_filter_factory import KalmanFilterFactory
from .utils.stopwatch_endpoint_factory import StopwatchEndpointFactory
from .utils.timeout_loop_factory import TimeoutLoopFactory

__all__ = [
    "CommsLoop",
    "SocketsListenerFactory",
    "SocketsLoopFactory",
    "SocketsWrapper",
    "PipeLoopFactory",
    "CommandProcessorFactory",
    "CommandReceiverFactory",
    "LocalConsole",
    "RemoteConsole",
    "RecorderFactory",
    "PageReader",
    "ReplayerFactory",
    "TextReader",
    "TextReplayerFactory",
    "KalmanFilterFactory",
    "StopwatchEndpointFactory",
    "TimeoutLoopFactory",
]
