'''The `RunnerProtocol` defines the interface for a wrapper that executes a
 `Node`.

By wrapping execution `Node`s, keyboard interrupts can be caught. Another
application of `Runner`s is to provide a CLI interface for running a `Node`.
These features are implemented in the concrete implementations of `Runner`s.
'''

from snr.types import *

from .config_protocol import ConfigProtocol


@runtime_checkable
class RunnerProtocol(Protocol):
    '''Protocol for wrapping execution of a `Node`
    '''

    config: ConfigProtocol
    '''The `Config` describing the Mode and component factories for a `Node`'''
    role: Role
    '''The role identifier of the Node executed by the `Runner`'''

    def run(self) -> None:
        '''Constructs and executes the `Node` specified by the `Runner`'s
        config and role'''
        ...
