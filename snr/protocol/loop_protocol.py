from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .component_protocol import ComponentProtocol
from .reloadable import Reloadable


@runtime_checkable
class LoopProtocol(ComponentProtocol, Reloadable, Protocol):
    """A Node component that runs outside the main thread event loop.

    Base loop implementation may use any concurrency style, ThreadLoop is
    provided. User implemented loops will inherit from base loops such as
    ThreadLoop.

    The loop lifecycle:
    Main thread                             Loop context
    1. Loop() - Constructed
    2. begin() - Started by Node
                                            3. setup() - Runs user setup
                                            4. loop_handler() - Runs its loop
    4. join() - Called from outside the
                loop to end it
    5. set_terminate_flag() - Signals loop
                              to end
                                            5. halt() - Cleans up after the
                                                        running loop, should
                                                        be reloadable now
    6. terminate() - Called by the Node to
                     clean the entire
                     module up

    The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def setup(self) -> None:
        '''User implemented method run at the beginning of the Loop's loop
        '''
        ...

    def loop_handler(self) -> None:
        '''User implemented method run per loop iteration
        '''
        ...

    def halt(self) -> None:
        '''User implemented function run to clean up loop, prepare for reload
        '''
        ...

    def set_terminate_flag(self) -> None:
        '''Base loop function to signal termination, used by join()
        '''
        ...

    def is_terminated(self) -> bool:
        '''Base loop function to indicate whether loop execution has finished
        '''
        ...
