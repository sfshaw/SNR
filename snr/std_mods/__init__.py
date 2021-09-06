'''This module provides a number of pre-made Endpoints and Loops for easy
 re-use. They should be imported via `snr` using `from snr import *`.

Some other classes may be available for additional imports.
'''

from snr.std_mods.comms import (CommsLoop, SocketsListenerFactory,
                                SocketsLoopFactory, SocketsWrapper)

from .comms.pipe.pipe_loop_factory import PipeLoopFactory
# from .filters import KalmanFilterFactory
from .filters import MovingAvgFilterFactory
from .io.console import LocalConsole, RemoteConsole
from .io.console.command_processor_factory import CommandProcessorFactory
from .io.console.command_receiver_factory import CommandReceiverFactory
from .io.recorder.recorder_endpoint_factory import RecorderEndpointFactory
from .io.replayer.page_reader import PageReader
from .io.replayer.replayer_loop_factory import ReplayerLoopFactory
from .io.replayer.text_reader import TextReader
from .io.replayer.text_replayer_factory import TextReplayerFactory
from .utils.stopwatch_endpoint_factory import StopwatchEndpointFactory
from .utils.timeout_loop_factory import TimeoutLoopFactory
from .io.printer.printer_endpoint_factory import PrinterEndpointFactory

__all__ = [
    "CommsLoop",
    "SocketsListenerFactory",
    "SocketsLoopFactory",
    "SocketsWrapper",
    "PipeLoopFactory",
    "MovingAvgFilterFactory",
    # "KalmanFilterFactory",
    "CommandProcessorFactory",
    "CommandReceiverFactory",
    "LocalConsole",
    "RemoteConsole",
    "RecorderEndpointFactory",
    "PageReader",
    "ReplayerLoopFactory",
    "TextReader",
    "TextReplayerFactory",
    "PrinterEndpointFactory",
    "StopwatchEndpointFactory",
    "TimeoutLoopFactory",
]
